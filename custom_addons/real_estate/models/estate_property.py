from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "real_estate.property"
    _description = "Real estate property model"
    _order = "selling_price desc"

    ##TODO: Add other constraints...
    _sql_constraints = [
        ("positive_expected_price", "CHECK(expected_price > 0)", "Expected price must be positive."),
        ("positive_selling_price", "CHECK(selling_price > 0)", "Selling price must be positive"), ##TODO: Error, not able to add this constraint, check why
        ("positive_bedrooms", "CHECK(bedrooms > 0)", "The number of bedrooms must be positive"),
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
    validity = fields.Integer("Validity (days)", default=7)
    status = fields.Selection(string="Status",selection=
        [
            ("active", "Active"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        copy=False,
        default="active"
    )

    #########################################################################################################
    # Computed fields
    #########################################################################################################

    total_area = fields.Integer("Total area (sqm)", compute="_compute_total_area", help="Sum of living and garden area")
    best_offer = fields.Float("Best offer", compute="_compute_best_offer")
    date_deadline = fields.Date("Date deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    number_of_offers = fields.Integer(compute="_compute_number_of_offers")
    number_of_non_refused_offers = fields.Integer(compute="_compute_number_of_non_refused_offers", store=True)

    #########################################################################################################
    # Relational fields 
    #########################################################################################################

    property_type_id = fields.Many2one(
        comodel_name="real_estate.property_type", 
        string="Type"
    )

    offer_ids = fields.One2many(
        comodel_name="real_estate.offer", 
        string="Property", 
        inverse_name="property_id"
    )

    seller_id = fields.Many2one(
        comodel_name="res.users",
        string="Seller",
        default=lambda self: self.env.user # The current user
    )

    buyer_id = fields.Many2one(
        comodel_name="real_estate.partner",
        string="Buyer",
        copy=False
    )

    tag_ids = fields.Many2many("real_estate.property_tag", "Tags")

    #########################################################################################################
    # Computed fields methods
    #########################################################################################################

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
            if property.offer_ids:
                offer_prices = [offer.price for offer in property.offer_ids if offer.status != "refused"]
                if len(offer_prices) > 0:
                    property.best_offer = max(offer_prices)
                else:
                    property.best_offer = 0    
            else:
                property.best_offer = 0

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)

    def _inverse_date_deadline(self):
        for property in self:
            property.validity = (property.date_deadline - fields.Date.today()).days

    #########################################################################################################
    # Python constraints
    #########################################################################################################

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
                raise ValidationError(_("Selling price cannot be lower than 90% of the expected price."))

    @api.constrains("expected_price")
    def _check_expected_price_positive(self):
        for property in self:
            if property.expected_price < 0:
                raise ValidationError(_("[Python constraint] Expected price cannot be negative."))

    #########################################################################################################
    # Onchange methods
    #########################################################################################################

    @api.onchange("garden")
    def _onchange_garden(self):
        ##TODO: When garden value changes the fields garden_area and garden_orientation should become readonly in the view.
        for property in self:
            if not property.garden:
                property.garden_area = 0;
                property.garden_orientation = None

    # @api.onchange("date_deadline")
    # def _onchange_date_deadline(self):
    #     ##TODO: Implement check if the date is in the past
    #     for property in self:
    #         return {
    #             "warning" : {
    #                 "title" : _("Date in the past"),
    #                 "message" : _("Date deadline cannot be in the past")
    #             }
    #         }
        
    #TODO: This would perform validation on frontend via AJAX
    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        ##TODO: Find out how to validate this field so that it must be positive
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
    
    ##TODO: This would perform validation on frontend via AJAX 
    # @api.onchange("garden_area")
    # def _onchange_garden_area(self):
    #     ##TODO: This forces the value of gardern area to be 0 if garden is False, but still the field is not readonly
    #     for property in self:
    #         if not property.garden:
    #             property.garden_area = 0 ##TODO: No business logic in onchange methods. Should this be here?
    #         elif property.garden_area < 0:
    #             property.garden_area = 0
    #             return {
    #                 "warning" : {
    #                     "title" : _("Negative value"),
    #                     "message" : _("Garden area cannot be negative")
    #                 }
    #             }
            
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
        ##TODO: This forces the value of gardern orientation to be None if garden is False, but still the field is not readonly
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
