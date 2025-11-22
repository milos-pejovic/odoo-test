from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime
import re


class FairMaterialProgram(models.Model):
    _name = "fair_material.fair_material_program"
    _description = "Fair material program"
    
    # Name of the Program e.g. "Fairtrade gold"
    name = fields.Char("Name", required=True)
    description = fields.Text(string="Description")
    date_of_establishment = fields.Date("Date of establishment", required=True)

    ##TODO: Does this refer to focus material stock from this program, or from all programs? 
    current_stock = fields.Integer(
        string="Current stock", 
        required=True, 
        default=0, 
        help="This material stock from this prorgam (not total stock). For total stock see the focus material page."
    )
    
    ##TODO: Should this be in the material's product.product record? 
    cost_per_gram = fields.Float(
        string="Cost per gram (USD)", 
        required=True, 
        default=0
    )

    ##TODO: Do wee need this?
    techincal_name = fields.Char(
        string="Technical name",
        compute="_compute_techincal_name"
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

    focus_material_id = fields.Many2one(
        comodel_name='product.template',
        string='Focus Material',
        required=True,
        domain=lambda self: [
            ('categ_id', '=', self.env.ref('fair_material.category_focus_materials').id)
        ]
    )

    @api.depends("name")
    def _compute_techincal_name(self):
        for record in self:
            record.techincal_name = record.to_snake_case(record.name)

    # Validate allocation range
    @api.constrains('default_allocation')
    def _check_allocation_range(self):
        for rec in self:
            if rec.default_allocation < 0 or rec.default_allocation > 100:
                raise UserError("Allocation must be between 0 and 100%.")

    def to_snake_case(self, text):
        """
        TODO: Move to a utils class
        Convert a string to snake_case
        """
        
        if not text:
            return ""
        text = re.sub(r'[^0-9a-zA-Z]+', '_', text)
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
        return text.lower().strip('_')

    @api.model
    def create(self, vals):
        """
        ##TODO: Create product related records needed
        """

        record = super(FairMaterialProgram, self).create(vals)

        template = record.focus_material_id
        if template:
            self.env['product.product'].create({
                'product_tmpl_id': template.id,
                'name': record.name
            })

        return record