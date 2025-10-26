from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare
import logging

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = "real_estate.property"
    _description = "Real estate property model"
    _order = "selling_price desc"

    ##TODO: Add other constraints...
    _sql_constraints = [
        ("positive_expected_price", "CHECK(expected_price > 0)", "Expected price must be positive."),
        ("positive_selling_price", "CHECK(selling_price IS NULL OR selling_price >= 0)", "Selling price must be positive"), ##TODO: Error, not able to add this constraint, check why
        ("positive_bedrooms", "CHECK(bedrooms >= 0)", "The number of bedrooms must not be negative."),
        ("positive_garden_area", "CHECK(garden_area >= 0)", "The garden area cannot be negative"),
        ("positive_living_area", "CHECK(living_area >= 0)", "The living area cannot be negative"),
    ]

    # These attributes are availiable to all field types:
    # string (str, default: field’s name)
    # The label of the field in UI (visible by users).

    # required (bool, default: False)
    # If True, the field can not be empty. It must either have a default value or always be given a value when creating a record.

    # help (str, default: "")
    # Provides long-form help tooltip for users in the UI.

    # index (bool, default: False)

    # Database fields
    name = fields.Char("Property name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Post code")
    date_availability = fields.Date("Date availability", help="Until when the property is available")
    date_sold = fields.Datetime("Date sold")
    expected_price = fields.Float("Expected price", required=True, default=0)
    selling_price = fields.Float("Selling price")
    bedrooms = fields.Integer("Bedrooms", help="The number of bedrooms")
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades", invisible=True) #TODO: Confirm: Hide in forms?
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(string="Garder orientation", selection=
        [
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"), 
            ("west", "West")
        ],
        copy=False # If this record is duplicated, this field will not be duplicated
    )
    date_deadline = fields.Date("Date deadline")
    
    ##TODO: Pogeldati copy metodu, dase se definse.. unikatna vrednost 
    status = fields.Selection(string="Status",selection=
        [
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        copy=False,
        default="new"
    )

    #########################################################################################################
    # Computed fields
    #########################################################################################################

    total_area = fields.Integer("Total area (sqm)", compute="_compute_total_area", help="Sum of living and garden area")
    best_offer = fields.Float("Best offer", compute="_compute_best_offer")
    validity = fields.Integer(string="Validity (days)", compute="_compute_validity", inverse="_inverse_validity")
    number_of_offers = fields.Integer(compute="_compute_number_of_offers")
    number_of_non_refused_offers = fields.Integer(compute="_compute_number_of_non_refused_offers", store=True)

    #########################################################################################################
    # Relational fields 
    #########################################################################################################

    property_type_id = fields.Many2one(
        comodel_name="real_estate.property_type", 
        string="Type",
        ondelete="set null"
    )

    offer_ids = fields.One2many(
        comodel_name="real_estate.offer", 
        string="Offers", 
        inverse_name="property_id",
    )

    seller_id = fields.Many2one(
        comodel_name="real_estate.seller",
        string="Seller",
        default=lambda self: self.env["real_estate.seller"].search([('user_id', '=', self.env.user.id)], limit=1) # The current real_estate.seller
    )

    buyer_id = fields.Many2one(
        comodel_name="real_estate.partner",
        string="Buyer",
        copy=False
    )

    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name="real_estate.property_tag"
    )

    #########################################################################################################
    # Computed fields methods
    #########################################################################################################

    ##TODO: If it is stored, the decorater is not needed
    @api.depends("offer_ids.status")
    def _compute_number_of_non_refused_offers(self):
        """ Get the number of offers that are not refused """
     
        for property in self:
            property.number_of_non_refused_offers = len([status for status in property.offer_ids.mapped("status") if not status in ("accepted", "refused")])

    @api.depends("offer_ids")
    def _compute_number_of_offers(self):
        for property in self:
            property.number_of_offers = len(property.offer_ids) if property.offer_ids else 0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        """ Get the price of the best offer that is not refused """

        for property in self:
            best_offer = 0
            if property.offer_ids:
                offer_prices = [offer.price for offer in property.offer_ids if offer.status != "refused"]
                if len(offer_prices) > 0:
                    best_offer = max(offer_prices)
            property.best_offer = best_offer
            
    @api.depends("date_deadline")
    def _compute_validity(self):
        for property in self:
            property.validity = (property.date_deadline - fields.Date.today()).days

    def _inverse_validity(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)

    #########################################################################################################
    # Python constraints
    #########################################################################################################

    @api.constrains("bedrooms")
    def _check_bedroom_number_positive(self):
        for property in self:
            if property.bedrooms and property.bedrooms < 0:
                raise ValidationError(_("[Python constraint] The number of bedroms cannot be negative."))

    @api.constrains("selling_price", "expected_price")
    def _check_selling_and_expected_price(self):
        """ Check if the selling price is at least 90% of the expected price """

        for property in self:
            if property.selling_price == 0:
                return
            
            diff = float_compare(
                (property.expected_price * 0.9), 
                property.selling_price, 
                precision_digits=4
            )

            if diff == 1:
                raise ValidationError(_("[Python constraint] Selling price cannot be lower than 90% of the expected price."))

    @api.constrains("expected_price")
    def _check_expected_price_positive(self):
        for property in self:
            if property.expected_price < 0:
                raise ValidationError(_("[Python constraint] Expected price cannot be negative."))

    @api.constrains("date_deadline")
    def _check_date_deadline_not_in_past(self):
        for property in self:
            if property.date_deadline < fields.Date.today():
                raise ValidationError(_("Date deadline cannot be in the past."))
            
    @api.constrains("validity")
    def _check_validity_not_negative(self):
        for property in self:
            if property.validity < 0:
                raise ValidationError(_("Validity cannot be negative."))

    #########################################################################################################
    # Onchange methods
    #########################################################################################################

    @api.onchange("garden")
    def _onchange_garden(self):
        ##TODO: When garden value changes the fields garden_area and garden_orientation should become readonly in the view.
        ##TODO: This has been achieved in the view itself.
        for property in self:
            if not property.garden:
                property.garden_area = 0;
                property.garden_orientation = None

    #TODO: This would perform validation on frontend via AJAX
    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        for property in self:
            if property.expected_price < 0:
                property.expected_price = abs(property.expected_price)
                return {
                    "warning" : {
                        "title" : _("Negative value"),
                        "message" : _("[on_change method] Expected price cannot be negative")
                    }
                }

    ##TODO: This would perform validation on frontend via AJAX 
    # @api.onchange("selling_price")
    # def _onchange_selling_price(self):
    #     ##TODO: Find out how to validate this field so that it must be positive
    #     for property in self:
    #         if property.selling_price < 0:
    #             property.selling_price = abs(property.selling_price)
    #             return {
    #                 "warning" : {
    #                     "title" : _("Negative value"),
    #                     "message" : _("Selling price cannot be negative")
    #                 }
    #             }
    
    #TODO: This would perform validation on frontend via AJAX 
    @api.onchange("garden_area")
    def _onchange_garden_area(self):
        ##TODO: This forces the value of gardern area to be 0 if garden is False, but still the field is not readonly
        for property in self:
            if not property.garden:
                property.garden_area = 0 ##TODO: No business logic in onchange methods. Should this be here?
            elif property.garden_area < 0:
                property.garden_area = 0
                return {
                    "warning" : {
                        "title" : _("Negative value"),
                        "message" : _("Garden area cannot be negative")
                    }
                }
            
    @api.onchange("living_area")
    def _onchange_living_area(self):
        for property in self:
            if property.living_area < 0:
                property.living_area = 0
                return {
                    "warning" : {
                        "title" : _("Negative value"),
                        "message" : _("Living area cannot be negative")
                    }
                }

    @api.onchange("garden_orientation")
    def _onchange_garden_orientation(self):
        for property in self:
            if not property.garden:
                property.garden_orientation = None ##TODO: No business logic in onchange methods. Should this be here?

    #########################################################################################################
    # Actions 
    #########################################################################################################

    def action_cancel(self):
        for property in self:
            if property.status == "sold":
                raise UserError(_("Cannot cancel a property that has already been sold."))
            property.status = "cancelled"
        return True

    def action_sold(self):
        for property in self:
            if property.status == "cancelled":
                raise UserError(_("Cannot sell a property that has been cancelled."))
            property.status = "sold"
        return True

    #########################################################################################################
    # CRUD
    #########################################################################################################

    def unlink(self):
        for property_record in self:
            if property_record.status == 'sold':
                _logger.info(f"Record {property_record.id} cannot be deleted due to status: {property_record.status}")
                raise UserError("Cannot delete a sold proeprty")
        return super().unlink()

    def update(self, vals):
        ## BIti pozvan sa UI 
        ##TODO: retko se koristi, za sada preskociti
        return super().update(vals)
