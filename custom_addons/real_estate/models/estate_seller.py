from odoo import fields, models, api


class EstateSeller(models.Model):
    _name = "real_estate.seller"
    _description = "Real estate seller"

    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        required=True
    )

    property_ids = fields.One2many(
        string="Real estate properties",
        comodel_name="real_estate.property",
        inverse_name="seller_id"
    )

    name = fields.Char(
        string="Name",
        related="user_id.partner_id.name", 
        readonly=False
    )

    email = fields.Char(
        string="Email",
        related="user_id.partner_id.email",
        readonly=False
    )

    properties_number = fields.Integer(
        string="Properties number",
        compute="_compute_properties_number"
    )

    def _compute_properties_number(self):
        for seller in self:
            seller.properties_number = len(seller.property_ids)