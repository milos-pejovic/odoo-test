{
    "name": "Fair material",
    "version": "1.0",
    "depends": ["base", "product", "mrp", "purchase", "sale_management", "stock", "account", "website_sale"],
    "author": "Milos Pejovic",
    "category": "Category",
    "description": """
    Practice module for Fair material.
    """,
    # data files always loaded at installation
    "data": [
        "security/ir.model.access.csv",
        "data/groups.xml",
        # "data/products.xml",
        "data/materials/focus_material_category.xml",
        "data/materials/gold.xml",
        "data/materials/tin.xml",

        # Actions first
        "views/focus_material_views.xml",
        "views/fair_material_program_views.xml",

        # Then the menu that references it
        "views/fm_menus.xml",
    ],
    # data files containing optionally loaded demonstration data
    "demo": [
        "demo/demo_data.xml",
    ],
    "application": True,
    "installable": True
}
