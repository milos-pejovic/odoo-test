from odoo import models, fields


class PropertyType(models.Model):
    _name = "real_estate.property_type"
    _description = "Real estate property type"
    _order = "sequence"

    name = fields.Char(string="Name", required=True)
    
    sequence = fields.Integer(string="Sequence", default=10) # Added myself
    