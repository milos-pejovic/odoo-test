from odoo import models, fields


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property model"
    _order = "sequence"

    # These attributes are availiable to all field types:
    # string (str, default: field’s name)
    # The label of the field in UI (visible by users).

    # required (bool, default: False)
    # If True, the field can not be empty. It must either have a default value or always be given a value when creating a record.

    # help (str, default: '')
    # Provides long-form help tooltip for users in the UI.

    # index (bool, default: False)

    name = fields.Char("Property name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Post code")
    date_availability = fields.Date("Date availability")
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("LIving area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage", default=False)
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(string="Garder orientation", selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
