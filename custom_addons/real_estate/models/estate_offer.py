from odoo import models, fields, _
from odoo.exceptions import UserError

class EstateOffer(models.Model):
    _name = "real_estate.offer"
    _description = "Offer for a cartain property"
    _order = "status"
    _sql_constraints = [("positive_price", "CHECK(price > 0)", "Offer price must be positive.")]

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
    type_id = fields.Many2one(related="property_id.property_type_id", store=True) ##TODO: Revise store=True here
    
    #########################################################################################################
    # Actions
    #########################################################################################################

    def action_accept(self):
        """ Called from the Property Offer list view. """
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError(_("An accepted offer already exists"))
        for offer in self.property_id.offer_ids:
            if not offer.status:
                offer.status = "refused"
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.status = "sold"
        return True ##TODO A public method should always return something so that it can be called through XML-RPC. When in doubt, just return True.

    def action_refuse(self):
        """ Called from the Property Offer list view. """
        self.ensure_one()
        if self.status == "accepted":
            raise UserError(_("This offer has already been accepted."))
        self.status = "refused"
        return True
