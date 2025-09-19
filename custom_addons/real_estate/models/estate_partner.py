from odoo import fields, models


class EstatePartner(models.Model):
    _name = "real_estate.partner"
    _description = "Real estate partner"
    _order = "sequence"

    name = fields.Char("Name", required=True)

    sequence = fields.Integer(default=10)
