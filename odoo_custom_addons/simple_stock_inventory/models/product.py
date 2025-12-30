from odoo import models, fields, api

class SSIProduct(models.Model):
    _name = 'ssi.product'
    _description = 'Produit Stock Simple'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom', required=True, tracking=True)
    default_code = fields.Char(string='Référence', tracking=True)
    barcode = fields.Char(string='Code-barres', tracking=True)
    cost_price = fields.Float(string='Prix de revient', tracking=True)
    sale_price = fields.Float(string='Prix de vente', tracking=True)
    qty_on_hand = fields.Float(string='Stock total', compute='_compute_qty_on_hand', store=True)
    quant_ids = fields.One2many('ssi.quant', 'product_id', string='Quants')
    move_ids = fields.One2many('ssi.move', 'product_id', string='Mouvements')

    @api.depends('quant_ids.quantity')
    def _compute_qty_on_hand(self):
        for product in self:
            product.qty_on_hand = sum(product.quant_ids.mapped('quantity'))
