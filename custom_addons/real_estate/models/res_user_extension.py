from odoo import models, fields

class ResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        string="Properties",
        comodel_name="real_estate.property",
        inverse_name="seller_id"
    )
