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

    @api.model_create_multi
    def create(self, vals_list):
        """Support both single and batch creation."""

        # Normalize input to a list of dicts
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        group_seller = self.env.ref("real_estate.group_seller")

        for vals in vals_list:
            if not vals.get("user_id"):
                name = vals.get("name") or "Unnamed"
                email = f"{name.lower().replace(' ', '_')}@example.com"

                partner = self.env["res.partner"].create({
                    "name": name,
                    "email": email,
                })

                user = self.env["res.users"].create({
                    "partner_id": partner.id,
                    "login": email,
                    "groups_id": [(4, group_seller.id)],
                })

                vals["user_id"] = user.id

        sellers = super().create(vals_list)
        return sellers
