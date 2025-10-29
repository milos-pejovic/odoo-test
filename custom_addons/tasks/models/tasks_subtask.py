from odoo import models, fields, api


class TasksSubtask(models.Model):
    _name = "tasks.subtask"
    _order = "sequence"

    title = fields.Char(string="Title", required=True)
    description = fields.Char(string="Description")
    sequence = fields.Integer(default=1)
    icon_x = fields.Html(string="X", compute="_compute_icon_x", sanitize=False)

    status = fields.Selection([
        ("in_progress", "In progress"),
        ("done", "Done"),
    ], default="in_progress")

    task_id = fields.Many2one(
        string="Task",
        comodel_name="tasks.task"
    )

    @api.depends()
    def _compute_icon_x(self):
        for rec in self:
            if rec.status == "in_progress":
                rec.icon_x = '<i class="fa fa-times" style="color: lightgray; font-size: 16px;"></i>'
            elif rec.status == "done":
                rec.icon_x = '<i class="fa fa-check" style="color: green; font-size: 16px;"></i>'
