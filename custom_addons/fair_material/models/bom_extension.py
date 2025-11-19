from odoo import models, fields


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    version_date = fields.Date(string="Version date", required=True)
