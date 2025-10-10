from odoo import http
from odoo.http import request
import html


class PropertyController(http.Controller):

    # @http.route("/property/inquiry/submit", type="http", methods=['POST'], auth='public', website=True)
    @http.route("/property/inquiry/submit", type="http", methods=['POST'], auth='public', website=True)
    def property_inquiry(self, **kwargs):        
        name = kwargs.get("name").strip()
        email = kwargs.get("email").strip()
        message = kwargs.get("message").strip()

        ##TODO: validate and sanitize user input

        errors = {}
        values = {}
        safe_message = html.escape(message)

        # Create the enquiry row in the DB
        # !!! Do this only if the validation succeeds
        # Sudo may be needed to assign create permissions
        # request.env['real_estate.property_inquiry'].sudo().create({
        #     "name" : name,
        #     "email" : email,
        #     "message" : message
        # })

        return request.render("property_inquiry_form", {
            "errors" : errors,
            "values" : values,
            "safe_message" : safe_message
        })

    # @http.route("/test", methods=["GET"], type="http", auth="public", website=True)
    @http.route("/test", methods=["GET"], type="http", auth="public", website=True)
    def test(self, **kwargs):
        return request.render("real_estate.test_view", {})
    