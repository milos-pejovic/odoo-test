from odoo import models, fields, tools


class PropertySellerReport(models.Model):
    _name = "real_estate.property_seller_report"
    _description = "Gives running values and stats for sellers"
    _auto = False

    id = fields.Integer("ID", readonly=True)
    seller_id = fields.Many2one(comodel_name="real_estate.seller", readonly=True)
    name = fields.Char("Property name", readonly=True)
    date_sold = fields.Datetime("Selling date", readonly=True)
    selling_price = fields.Float("Selling price", readonly=True)
    running_total = fields.Float("Running total", readonly=True)
    running_average = fields.Float("Running average", readonly=True)
    order_of_selling = fields.Integer("Order of selling")
    running_lowest = fields.Float("Running lowest", readonly=True)
    running_highest = fields.Float("Running highest", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, "real_estate_property_seller_report")
        self._cr.execute("""
           CREATE OR REPLACE VIEW real_estate_property_seller_report AS (
                SELECT
                    id,
                    seller_id,
                    date_sold,
                    name,
                    selling_price,
                    ROW_NUMBER() OVER (PARTITION BY seller_id ORDER BY date_sold) as order_of_selling,
                    SUM(selling_price) OVER (PARTITION BY seller_id ORDER BY date_sold) as running_total,
                    AVG(selling_price) OVER (PARTITION BY seller_id ORDER BY date_sold) as running_average,
                    MIN(selling_price) OVER (PARTITION BY seller_id ORDER BY date_sold) as running_lowest,
                    MAX(selling_price) OVER (PARTITION BY seller_id ORDER BY date_sold) as running_highest
                FROM real_estate_property
                WHERE selling_price > 0
                ORDER BY seller_id
            )                       
        """)
