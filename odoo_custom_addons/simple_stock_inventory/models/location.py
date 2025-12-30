from odoo import models, fields

class SSILocation(models.Model):
    _name = 'ssi.location'
    _description = 'Emplacement Stock Simple'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom', required=True, tracking=True)
    usage = fields.Selection([
        ('internal', 'Interne'),
        ('supplier', 'Fournisseur'),
        ('customer', 'Client'),
        ('inventory', 'Ajustement Inventaire'),
    ], string='Usage', default='internal', required=True, tracking=True)
    active = fields.Boolean(string='Actif', default=True, tracking=True)
