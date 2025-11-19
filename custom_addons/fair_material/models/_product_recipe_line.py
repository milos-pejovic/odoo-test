from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductRecipeLine(models.Model):
    """
    Manufacturing BOM Line will be used instead of this
    """

    _name = "fair_material.product_recipe_line"
    _description = "Product recipe line "

    product_recipe_id = fields.Many2one(
        string="Product recipe",
        comodel_name="fair_material.product_recipe",
        required=True
    )

    focus_material_id = fields.Many2one(
        string="Focus material",
        comodel_name="fair_material.focus_material",
        required=True
    )

    amount = fields.Float(
        string="Amount (grams)",
        required=True,
        default=0
    )

    ###################################################################################################
    # Field contsraints
    ###################################################################################################

    # Constraint: amount must be >= 0
    @api.constrains("amount")
    def _check_amount_non_negative(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError("Amount of material cannot be negative.")
