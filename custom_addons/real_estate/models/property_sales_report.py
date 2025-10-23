from odoo import fields, models, tools

class PropertySalesReport(models.Model):
    _name = "real_estate.property_sales_report"
    _description = "lorem ipsum"
    _auto = False

    id = fields.Integer("ID", readonly=True)
    seller_id = fields.Many2one(comodel_name="res.users", string="Salesperosn", readonly=True)
    property_count = fields.Integer(string="Number of properties", readonly=True)
    total_value = fields.Float(string="Total property value", readonly=True)
    new_properties = fields.Integer(string="New", readonly=True)
    average_selling_price = fields.Float(string="Average", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, "real_estate_property_sales_report")
        self._cr.execute("""
           CREATE OR REPLACE VIEW real_estate_property_sales_report AS (
                SELECT
                    seller_id AS id,
                    seller_id,
                    COUNT(*) AS property_count,
                    COUNT(CASE WHEN status = 'new' THEN id END) AS new_properties,
                    COALESCE(SUM(selling_price), 0) AS total_value,
                    COALESCE(AVG(CASE WHEN status = 'sold' THEN selling_price END), 0) AS average_selling_price
                FROM real_estate_property
                GROUP BY seller_id
            )              
        """)







# from odoo import fields, models, tools


# class PropertySalesReport(models.Model):
#     _name = "real_estate.property_sales_report"
#     _description = "Property sales report"
#     _auto = False # This tells Odoo this is not a Model but an SQL view and that a new database table should NOT be created

#     id = fields.Integer("ID", readonly=True)
#     seller_id = fields.Many2one("res.users", string="Salesperson", readonly=True)
#     property_count = fields.Integer("Number of Properties", readonly=True)
#     total_value = fields.Float("Total Property Value", readonly=True)

#     def init(self):
#         """
#         Every SQL view must have an init method that defines the SQL for the view creation.
#         """

#         tools.drop_view_if_exists(self._cr, 'real_estate_property_sales_report')

#         # This view will return exactly one row per seller_id so using seller_id as id is acceptable
#         self._cr.execute("""
#             CREATE OR REPLACE VIEW real_estate_property_sales_report AS (
#                 SELECT
#                     seller_id as id,
#                     seller_id,
#                     COUNT(*) AS property_count,
#                     COALESCE(SUM(selling_price), 0) AS total_value
#                 FROM real_estate_property
#                 GROUP BY seller_id
#             )
#         """)

# self._cr.execute("""
#     CREATE OR REPLACE VIEW real_estate_property_sales_report AS (
#         SELECT
#             row_number() OVER () AS id,
#             seller_id as id,
#             seller_id,
#             COUNT(*) AS property_count,
#             COALESCE(SUM(selling_price), 0) AS total_value
#         FROM real_estate_property
#         GROUP BY seller_id
#     )
# """)






# Explain window functions

# why
# COALESCE(SUM(selling_price), 0) AS total_value
# Makes sure we don't get a NULL, but 0 

# WHat happens if a record has no seller_id


# ARe both of tehse necessary?
#  tools.drop_view_if_exists(self._cr, 'real_estate_property_sales_report')
# CREATE OR REPLACE VIEW real_estate_property_sales_report AS (



### WINDOW FUNCTIONS:
# row_number()
# OVER()