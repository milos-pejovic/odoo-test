from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime


class FairMaterialProgram(models.Model):
    _name = "fair_material.fair_material_program"
    _description = "Fair material program"
    
    # Name of the Program e.g. "Fairtrade gold"
    name = fields.Char("Name", required=True)
    description = fields.Text("Description", required=False)
    date_of_establishment = fields.Date("Date of establishment", required=True)

    ##TODO: Does this refer to focus material stock from this program, or from all programs? 
    current_stock = fields.Integer(
        string="Current stock", 
        required=True, 
        default=0, 
        help="This material stock from this prorgam (not total stock). For total stock see the focus material page."
    )
    
    cost_per_gram = fields.Float(
        string="Cost per gram (USD)", 
        required=True, 
        default=0
    )

    ##TODO: This needs to be set per product
    # Implement Many2Many 
    ##TODO; constraint to 0.0 - 100.0
    ##TODO: remember to use Odoo's float methods
    default_allocation = fields.Float(
        string="Allocation", 
        required=True, 
        default=100.0, 
        help="Default allocation for all products. Can be overriden on a per product basis."
    )

    # Focus material e.g. gold
    focus_material_id = fields.Many2one(
        string="Focus material",
        comodel_name="product.product",
        required=True
    )

    ###################################################################################################
    # Field contsraints
    ###################################################################################################

    # Validate allocation range
    @api.constrains('default_allocation')
    def _check_allocation_range(self):
        for rec in self:
            if rec.default_allocation < 0 or rec.default_allocation > 100:
                raise UserError("Allocation must be between 0 and 100%.")
