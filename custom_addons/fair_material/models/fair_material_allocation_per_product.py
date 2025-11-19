from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime


class FairMaterialAllocationPerProduct(models.Model):
    _name = "fair_material.fair_material_allocation_per_product"
    _description = "Fair material allocation per product"
    
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True
    )

    fair_material_program_id = fields.Many2one(
        comodel_name="fair_material.fair_material_program",
        string="Fair Material Program",
        required=True
    )

    allocation_percent = fields.Float(
        string="Allocation %",
        default=100.0,
        digits=(3,2),
        help="Percentage of this material program used for this product"
    )

    ##TODO: constrain allocation_percent to 0.0 - 100.0
    ##TODO: add check that all fair material allocations for the given materila must not be greater than 100%. CHeck if they can be lower than 100%