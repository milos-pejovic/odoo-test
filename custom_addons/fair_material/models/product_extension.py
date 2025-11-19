from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Product BOM covers this
    # product_recipe_ids = fields.Many2many(
    #     comodel_name='fair_material.product_recipe',
    #     relation='product_recipe_rel',
    #     column1='product_id',
    #     column2='recipe_id',
    #     string='Material Recipes'
    # )

    material_allocation_ids = fields.One2many(
        comodel_name='fair_material.fair_material_allocation_per_product',
        inverse_name='product_id',
        string='Fair Material Allocations'
    )
