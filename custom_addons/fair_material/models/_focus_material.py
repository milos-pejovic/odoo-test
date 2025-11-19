from odoo import models, fields


class FocusMaterial(models.Model):
    """
    Focus material will be a type of product in order to leverage Odoo's built in product functionalitis (procurement, stock tracking etc).
    """

    _name = "fair_material.focus_material"
    _description = "Focus material such as gold, silver, cobalt..."
    
    name = fields.Char("Name", required=True)

    fair_material_program_ids = fields.One2many(
        string="Fair material programs",
        comodel_name="fair_material.fair_material_program",
        inverse_name="focus_material_id"
    )

    ##TODO: Calculate total stock by adding up stocks from all FMPs  
    # amount = fields.Integer("amount", required=True, help="In grams")

    ##TODO: recipe_ids