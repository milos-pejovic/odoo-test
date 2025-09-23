from odoo import models, fields


class PropertyType(models.Model):
    _name = "real_estate.property_type"
    _description = "Real estate property type"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        comodel_name="real_estate.property", 
        inverse_name="property_type_id", 
        string="Properties"
    )
