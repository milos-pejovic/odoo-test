from odoo import models, fields


class ResUser(models.Model):
    _inherit = "res.users"

    seller_ids = fields.One2many(
        string="Seller profiles",
        comodel_name="real_estate.seller",
        inverse_name="user_id"
    )

    buyer_ids = fields.One2many(
        string="Buyer profiles",
        comodel_name="real_estate.buyer",
        inverse_name="user_id"
    )
