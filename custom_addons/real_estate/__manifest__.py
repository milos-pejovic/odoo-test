{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base", "website", "base"],
    "author": "Milos Pejovic",
    "category": "Category",
    "description": """
    Practice module made by following the documentation on Odoo website https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101/02_newapp.html
    """,
    # data files always loaded at installation
    "data": [
        "security/ir.model.access.csv",
        
        # Actions first
        "views/estate_property_views.xml",
        "views/estate_property_types_views.xml",
        "views/estate_offers_views.xml",
        "views/estate_partner.xml",
        "views/estate_buyers_view.xml",
        "views/estate_property_tag.xml",
        "views/estate_development.xml",
        "views/res_users.xml",
        "views/property_inquiry_form.xml",
        "views/test_view.xml",
        "views/property_sales_report_views.xml",
        "views/property_seller_report_view.xml",

        # Then the menu that references it
        "views/estate_menus.xml",
    ],
    # data files containing optionally loaded demonstration data
    "demo": [
        "demo/demo_data.xml",
    ],
    "application": True,
    "installable": True
}
