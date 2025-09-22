from odoo import fields, models


class EstatePartner(models.Model):
    _name = "real_estate.partner"
    _description = "Real estate partner"
    _order = "name"

    name = fields.Char("Name", required=True)
