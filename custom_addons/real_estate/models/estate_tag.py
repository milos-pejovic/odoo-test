from odoo import fields, models


class PropertyTag(models.Model):
    _name = "real_estate.property_tag"
    _description = "Proeprty tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.Many2many("real_estate.property", "Properties")
