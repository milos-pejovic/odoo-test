from odoo import models, fields


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    focus_material_id = fields.Many2one(
        comodel_name="product.product",
        string='Focus Material'
    )

    ##TODO: The Manufacturing module works with a single product per BOM. Modification/extension may be required.
    # New field to link multiple specific product variants to this BOM
    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Applicable Products',
        help='List of product variants this BOM applies to.'
    )

    # Amount
    # Bom line already has "product_qty" field which can be used for quantity