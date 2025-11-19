from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime


class FocusMaterial(models.Model):
    _name = "fair_material.focus_material"
    _description = "Focus material"
    
    name = fields.Char("Name", required=True)

    fair_material_program_ids = fields.One2many(
        string="Fair material programs",
        comodel_name="fair_material.fair_material_program",
        inverse_name="focus_material_id"
    )

    ##TODO: Product recipes

    ##TODO: Calculate total stock by adding up stocks from all FMPs  
    # amount = fields.Integer("amount", required=True, help="In grams")

    ##TODO: recipe_ids