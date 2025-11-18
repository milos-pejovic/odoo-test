{
    "name": "Fair material",
    "version": "1.0",
    "depends": ["base", "website"],
    "author": "Milos Pejovic",
    "category": "Category",
    "description": """
    Practice module for Fair material
    """,
    # data files always loaded at installation
    "data": [
        "data/groups.xml",

        "security/ir.model.access.csv",

        # Actions first


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
