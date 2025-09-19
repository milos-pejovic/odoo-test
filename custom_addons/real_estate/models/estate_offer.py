from odoo import models, fields


class EstateOffer(models.Model):
    _name = "real_estate.offer"
    _description = "Offer for a cartain property"
    _order = "sequence"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one("real_estate.partner", required=True)
    property_id = fields.Many2one("real_estate.property", required=True)
    type_id = fields.Many2one(related="property_id.property_type_id", store=True) # TODO: Check what this does
    
    sequence = fields.Integer(default=10)
    