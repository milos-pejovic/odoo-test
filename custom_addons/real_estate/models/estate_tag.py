from odoo import fields, models


class PropertyTag(models.Model):
    _name = "real_estate.property_tag"
    _description = "Proeprty tag"
    _order = "name"
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Tag name must be unique")
    ]

    name = fields.Char(string="Name", required=True)
    property_ids = fields.Many2many("real_estate.property", "Properties")
    