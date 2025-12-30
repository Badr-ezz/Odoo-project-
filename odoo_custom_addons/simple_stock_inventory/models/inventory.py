from odoo import models, fields, api

class SSIInventory(models.Model):
    _name = 'ssi.inventory'
    _description = 'Inventaire Stock Simple'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: self._get_next_sequence())
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    location_id = fields.Many2one('ssi.location', string='Emplacement', required=True, domain=[('usage', '=', 'internal')])
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('done', 'Validé'),
    ], string='État', default='draft', tracking=True)
    line_ids = fields.One2many('ssi.inventory.line', 'inventory_id', string='Lignes')

    @api.model
    def _get_next_sequence(self):
        return self.env['ir.sequence'].next_by_code('ssi.inventory') or 'INV-00001'

    def action_add_all_products(self):
        for inventory in self:
            existing_products = inventory.line_ids.mapped('product_id')
            all_products = self.env['ssi.product'].search([])
            new_products = all_products - existing_products
            for product in new_products:
                quant = self.env['ssi.quant'].search([
                    ('product_id', '=', product.id),
                    ('location_id', '=', inventory.location_id.id)
                ], limit=1)
                theoretical_qty = quant.quantity if quant else 0.0
                self.env['ssi.inventory.line'].create({
                    'inventory_id': inventory.id,
                    'product_id': product.id,
                    'theoretical_qty': theoretical_qty,
                })

    def action_validate(self):
        for inventory in self:
            if inventory.state != 'draft':
                continue
            for line in inventory.line_ids:
                diff = line.counted_qty - line.theoretical_qty
                if diff != 0:
                    # Générer move d'ajustement
                    location_inventory = self.env['ssi.location'].search([('usage', '=', 'inventory')], limit=1)
                    if not location_inventory:
                        continue
                    if diff > 0:
                        # Ajouter stock
                        move_vals = {
                            'product_id': line.product_id.id,
                            'location_from_id': location_inventory.id,
                            'location_to_id': inventory.location_id.id,
                            'quantity': diff,
                        }
                    else:
                        # Retirer stock
                        move_vals = {
                            'product_id': line.product_id.id,
                            'location_from_id': inventory.location_id.id,
                            'location_to_id': location_inventory.id,
                            'quantity': -diff,
                        }
                    move = self.env['ssi.move'].create(move_vals)
                    move.action_done()
            inventory.state = 'done'

class SSIInventoryLine(models.Model):
    _name = 'ssi.inventory.line'
    _description = 'Ligne Inventaire Stock Simple'

    inventory_id = fields.Many2one('ssi.inventory', string='Inventaire', required=True, ondelete='cascade')
    product_id = fields.Many2one('ssi.product', string='Produit', required=True)
    theoretical_qty = fields.Float(string='Quantité théorique', readonly=True)
    counted_qty = fields.Float(string='Quantité comptée', default=0.0)
    difference = fields.Float(string='Écart', compute='_compute_difference', store=True)

    @api.depends('theoretical_qty', 'counted_qty')
    def _compute_difference(self):
        for line in self:
            line.difference = line.counted_qty - line.theoretical_qty
