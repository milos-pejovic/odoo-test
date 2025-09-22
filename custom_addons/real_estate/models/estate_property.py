from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "real_estate.property"
    _description = "Real estate property model"
    _order = "selling_price desc"

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
    date_availability = fields.Date("Date availability")
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price")
    bedrooms = fields.Integer("Bedrooms")
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
    sequence = fields.Integer(string="Sequence", default=10) # Added myself

    #########################################################################################################
    # Computed fields
    #########################################################################################################

    total_area = fields.Integer("Total area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float("Best offer", compute="_compute_best_offer")
    date_deadline = fields.Date("Date deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    number_of_offers = fields.Integer(compute="_compute_number_of_offers")

    #########################################################################################################
    # Relational fields 
    #########################################################################################################

    property_type_id = fields.Many2one(comodel_name="real_estate.property_type", string="Type")
    offer_ids = fields.One2many("real_estate.offer", "property_id")
    seller_id = fields.Many2one(
        "res.users",
        string="Seller",
        default=lambda self: self.env.user # The current user
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )

    tag_ids = fields.Many2many("real_estate.property_tag", "Tags")

    #########################################################################################################
    # Computed fields methods
    #########################################################################################################

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
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price")) if property.offer_ids else 0

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)

    def _inverse_date_deadline(self):
        for property in self:
            property.validity = (property.date_deadline - fields.Date.today()).days

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

    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        ##TODO: Implement check if the date is in the past
        for property in self:
            return {
                "warning" : {
                    "title" : _("Date in the past"),
                    "message" : _("Date deadline cannot be in the past")
                }
            }
        
    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        ##TODO: Find out how to validate this field so that it must be positive
        for property in self:
            if property.expected_price < 0:
                property.expected_price = abs(property.expected_price)
                return {
                    "warning" : {
                        "title" : _("Negative value"),
                        "message" : _("Expected price cannot be negative")
                    }
                }
            
    @api.onchange("selling_price")
    def _onchange_selling_price(self):
        ##TODO: Find out how to validate this field so that it must be positive
        for property in self:
            if property.selling_price < 0:
                property.selling_price = abs(property.selling_price)
                return {
                    "warning" : {
                        "title" : _("Negative value"),
                        "message" : _("Selling price cannot be negative")
                    }
                }
    
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
                        "message" : _("Lviiving area cannot be negative")
                    }
                }

    @api.onchange("garden_orientation")
    def _onchange_garden_orientation(self):
        ##TODO: This forces the value of gardern orientation to be None if garden is False, but still the field is not readonly
        for property in self:
            if not property.garden:
                property.garden_orientation = None ##TODO: No business logic in onchange methods. Should this be here?
