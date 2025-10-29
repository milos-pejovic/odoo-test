from odoo import fields, models, api


class EstateBuyer(models.Model):
    _name = "real_estate.buyer"
    _description = "Real estate buyer"

    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        required=True
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

    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="real_estate.offer",
        inverse_name="buyer_id"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Support both single and batch creation."""

        # Normalize input to a list of dicts
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        group_buyer = self.env.ref("real_estate.group_buyer")

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
                    "groups_id": [(4, group_buyer.id)],
                })

                vals["user_id"] = user.id

        sellers = super().create(vals_list)
        return sellers
