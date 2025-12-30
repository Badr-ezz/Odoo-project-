from odoo import models, fields

class SSIQuant(models.Model):
    _name = 'ssi.quant'
    _description = 'Quant Stock Simple'
    _sql_constraints = [
        ('unique_product_location', 'unique(product_id, location_id)', 'Un quant existe déjà pour ce produit et cet emplacement.'),
    ]

    product_id = fields.Many2one('ssi.product', string='Produit', required=True, ondelete='cascade')
    location_id = fields.Many2one('ssi.location', string='Emplacement', required=True, ondelete='cascade')
    quantity = fields.Float(string='Quantité', default=0.0)
