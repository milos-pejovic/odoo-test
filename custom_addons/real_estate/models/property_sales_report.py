from odoo import fields, models, tools

class PropertySalesReport(models.Model):
    _name = "real_estate.property_sales_report"
    _auto = False

    id = fields.Integer("ID", readonly=True)
    seller_id = fields.Many2one(comodel_name="res.users", readonly=True)
    property_count = fields.Integer(string="Number of properties", readonly=True)
    total_value = fields.Float("Total value", readonly=True)
    sold_properties = fields.Integer("New properties")
    average_selling_price = fields.Float(string="Average", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, "real_estate_property_sales_report")
        self._cr.execute("""
            CREATE OR REPLACE VIEW real_estate_property_sales_report AS (
                SELECT
                    seller_id AS id,
                    seller_id,
                    COUNT(*) AS property_count,
                    COALESCE(COUNT(CASE WHEN status = 'sold' THEN id END), 0) as sold_properties,
                    COALESCE(SUM(selling_price), 0) AS total_value,
                    COALESCE(AVG(CASE WHEN status = 'sold' THEN selling_price END), 0) AS average_selling_price
                FROM real_estate_property
                GROUP BY seller_id      
            )
        """)






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


# Look at this query. I want a similar query that will utilize SQL window functions to show the history of a sellers


# CREATE OR REPLACE VIEW real_estate_property_sales_report AS (
#                 SELECT
#                     seller_id AS id,
#                     seller_id,
#                     COUNT(*) AS property_count,
#                     COALESCE(COUNT(CASE WHEN status = 'new' THEN id END), 0) as new_properties,
#                     COALESCE(SUM(selling_price), 0) AS total_value,
#                     COALESCE(AVG(CASE WHEN status = 'sold' THEN selling_price END), 0) AS average_selling_price
#                 FROM real_estate_property
#                 GROUP BY seller_id      
#             )

# SUM OVER (PARTITION BY selling_price ORDER BY selling_price) AS total_sales