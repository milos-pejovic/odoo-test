{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "Milos Pejovic",
    "category": "Category",
    "description": """
    Practice module made by following the documentation on Odoo website https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101/02_newapp.html
    """,
    # data files always loaded at installation
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml", # Action first
        "views/estate_menus.xml" # Then the menu that references it
    ],
    # data files containing optionally loaded demonstration data
    "demo": [
        "demo/demo_data.xml",
    ],
    "application": True,
    "installable": True
}
