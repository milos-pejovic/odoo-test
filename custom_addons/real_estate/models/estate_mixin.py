from odoo import models, fields

class EstateMixin(models.Model):
    _name = "real_estate.mixin"

    name = fields.Char(string="name", required=True)