from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime


class Product(models.Model):
    ##TODO: Extend the Product from Odoo

    _name = "fair_material.product"
    _description = "Fair material product"

    name = fields.Char("Name", required=True)

    ##TODO: check how many recipes a product can have at any moment
    product_recipe_ids = fields.Many2many(
        string="Recipes",
        comodel_name="fair_material.product_recipe"
    )
    ##TODO: Finish...

    ##TODO: recipe_ids