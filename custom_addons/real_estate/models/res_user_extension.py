from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        string="Real estate properties",
        comodel_name="real_estate.property",
        inverse_name="seller_id"
    )
