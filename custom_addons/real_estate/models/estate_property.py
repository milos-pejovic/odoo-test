from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "real_estate.property"
    _description = "Real estate property model"
    _order = "sequence"

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
    facades = fields.Integer("Facades", invicible=True) #TODO: Confirm:  Hide in forms?
    garage = fields.Boolean("Garage", default=False)
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
    sequence = fields.Integer(string="Sequence", default=10) # Added myself

    # Computed fields
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

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
    # Computed fields
    #########################################################################################################

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
