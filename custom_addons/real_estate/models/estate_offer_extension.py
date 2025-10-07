from odoo import models, fields

class EstateOfferExtension(models.Model):
    _inherit = "real_estate.offer"

    account_move_id = fields.Many2one("account.move")
