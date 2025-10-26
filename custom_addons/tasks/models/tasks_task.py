from odoo import models, fields, api

class TasksTask(models.Model):
    _name = "tasks.task"
    _description = "Task"

    title = fields.Char(string="Title", required=True)
    description = fields.Char(string="Description")

    status = fields.Selection(string="Status", selection=[
        ("1_groomed", "Groomed"),
        ("2_in_progress", "In progress"),
        ("3_testing", "Testing"),
        ("4_on_hold", "On hold"),
        ("5_done", "Done")
    ], default="1_groomed")

    type = fields.Selection(string="Type", selection=[
        ("backend", "Backend"),
        ("frontend", "Frontend/template"),
        ("website", "Website"),
        ("usage", "Usage"),
        ("other", "Other"),
        ("research", "Research")
    ])

    priority = fields.Selection(string="Priority", selection=[
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ])

    status_sequence = fields.Integer("Status Sequence", compute="_compute_status_sequence", store=True)

    @api.depends("status")
    def _compute_status_sequence(self):
        sequence_map = {
            "groomed": 1,
            "in_progress": 2,
            "testing": 3,
            "on_hold": 4,
            "done": 5,
        }
        for rec in self:
            rec.status_sequence = sequence_map.get(rec.status, 99)