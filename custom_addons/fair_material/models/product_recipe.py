from odoo import models, fields, api


class ProductRecipe(models.Model):
    _name = "fair_material.product_recipe"
    _description = "The list of all focus materials and their amounts needed to make a defined number of products"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=False)

    version_date = fields.Date(string="Version date", required=True)
    batch_size = fields.Integer(string="Batch size", required=True, default=1, help="The ammount of products the recipe is for")

    product_ids = fields.Many2many(
        string="Products",
        comodel_name="fair_material.product",
        relation="fair_material_recipe_product_rel",
        column1="recipe_id",
        column2="product_id",
    )

    recipe_line_ids = fields.One2many(
        string= "Materials needed",
        comodel_name="fair_material.product_recipe_line",
        inverse_name="product_recipe_id" 
    )
