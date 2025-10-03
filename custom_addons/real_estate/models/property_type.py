from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PropertyType(models.Model):
    _name = "real_estate.property_type"
    _description = "Real estate property type"
    _order = "sequence"
    _sql_constraints = [("unique_type_name", "UNIQUE(name)", "Property type name must be unique")]

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        comodel_name="real_estate.property", 
        inverse_name="property_type_id", 
        string="Properties"
    )
    sequence = fields.Integer(default=1)

    @api.model_create_multi
    def create(self, vals_list):
        new_types = super().create(vals_list)
        for vals in vals_list:
            self.env["real_estate.property_tag"].create({
                "name" : vals.get("name")
            })
        return new_types

    @api.ondelete(at_uninstall=False)
    def _on_delete_cancel_properties(self):
        # We do not iterate through self because:
        # The logic id the same for all records
        # Since we write into teh DB, vectorized approach is faster, one SQL query for all records. Iteration would have one query per record
        _logger.info(f"[ondelete] Cancelling properties.")
        self.mapped('property_ids').write({'status': 'cancelled'})

    def unlink(self):
        # If we want per record logging we need iteration. Otherwise we could sue vectorized approach.
        for item in self:
            _logger.info(f"[unlink] Deleting Type record {item.name}.");
        return super().unlink()
