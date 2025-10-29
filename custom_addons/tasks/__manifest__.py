{
    "name": "Tasks",
    "version": "1.0",
    "depends": ["base"],
    "author": "Milos Pejovic",
    "category": "Category",
    "description": """
    """,
    # data files always loaded at installation
    "assets" : {
        "web.assets_backend" : [
            "tasks/static/src/css/style.css"
        ]
    },
    "data": [
        "security/ir.model.access.csv",
        
        # Actions first
        "views/tasks_views.xml",

        # Then the menu that references it
        "views/tasks_menus.xml"
    ],
    # data files containing optionally loaded demonstration data
    "demo": [
        "demo/demo_data.xml",
    ],
    "application": True,
    "installable": True
}
