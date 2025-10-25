from odoo import models, fields


##TODO: abstract model
##TODO: see transient model
class EstateMixin(models.Model):
    _name = "real_estate.mixin"

    name = fields.Char(string="name", required=True)
