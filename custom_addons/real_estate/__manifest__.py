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
        "views/mymodule_view.xml",
        "security/ir.model.aacess.csv"
    ],
    # data files containing optionally loaded demonstration data
    "demo": [
        "demo/demo_data.xml",
    ],
    "application": True,
}
