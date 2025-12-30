from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SSIMove(models.Model):
    _name = 'ssi.move'
    _description = 'Mouvement Stock Simple'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: self._get_next_sequence())
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    product_id = fields.Many2one('ssi.product', string='Produit', required=True)
    location_from_id = fields.Many2one('ssi.location', string='Emplacement source')
    location_to_id = fields.Many2one('ssi.location', string='Emplacement destination', required=True)
    quantity = fields.Float(string='Quantité', required=True)
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('done', 'Validé'),
        ('cancel', 'Annulé'),
    ], string='État', default='draft', tracking=True)
    move_type = fields.Selection([
        ('in', 'Entrée'),
        ('out', 'Sortie'),
        ('transfer', 'Transfert'),
        ('adjust', 'Ajustement'),
    ], string='Type', compute='_compute_move_type', store=True)

    @api.model
    def _get_next_sequence(self):
        return self.env['ir.sequence'].next_by_code('ssi.move') or 'MOVE-00001'

    @api.depends('location_from_id.usage', 'location_to_id.usage')
    def _compute_move_type(self):
        for move in self:
            from_usage = move.location_from_id.usage if move.location_from_id else None
            to_usage = move.location_to_id.usage
            if from_usage == 'supplier' or (not from_usage and to_usage == 'internal'):
                move.move_type = 'in'
            elif to_usage == 'customer' or (from_usage == 'internal' and not to_usage):
                move.move_type = 'out'
            elif from_usage == 'internal' and to_usage == 'internal':
                move.move_type = 'transfer'
            else:
                move.move_type = 'adjust'

    @api.constrains('quantity')
    def _check_quantity(self):
        for move in self:
            if move.quantity <= 0:
                raise ValidationError("La quantité doit être positive.")

    def action_done(self):
        for move in self:
            if move.state != 'draft':
                continue
            # Vérifier stock si sortie d'un emplacement internal
            if move.location_from_id and move.location_from_id.usage == 'internal':
                quant = self.env['ssi.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_from_id.id)
                ], limit=1)
                if quant.quantity < move.quantity:
                    raise UserError("Stock insuffisant à la source.")
                quant.quantity -= move.quantity
            # Mettre à jour destination si internal
            if move.location_to_id.usage == 'internal':
                quant = self.env['ssi.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_to_id.id)
                ], limit=1)
                if not quant:
                    quant = self.env['ssi.quant'].create({
                        'product_id': move.product_id.id,
                        'location_id': move.location_to_id.id,
                        'quantity': 0.0,
                    })
                quant.quantity += move.quantity
            move.state = 'done'

    def action_cancel(self):
        for move in self:
            if move.state != 'done':
                continue
            # Réverser les quants
            if move.location_from_id and move.location_from_id.usage == 'internal':
                quant = self.env['ssi.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_from_id.id)
                ], limit=1)
                if quant:
                    quant.quantity += move.quantity
            if move.location_to_id.usage == 'internal':
                quant = self.env['ssi.quant'].search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_to_id.id)
                ], limit=1)
                if quant:
                    quant.quantity -= move.quantity
            move.state = 'cancel'
