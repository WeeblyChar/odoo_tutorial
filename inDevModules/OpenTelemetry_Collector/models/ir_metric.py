import datetime
import logging
from ast import literal_eval

import psutil
from odoo import _, api, fields, models
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Metric(models.Model):
    _name = "ir.metric"
    _description = "Metrics"

    name = fields.Char(required=True)
    description = fields.Char()
    active = fields.Boolean(
        default=True,
        help="""Activate or Deactivate the print action button.
                If no active then move to the status \'archive\'.
                Still can by found using filters button""",
    )
    metric_type = fields.Selection(
        [
            ("gauge", "Gauge"),
            ("counter", "Counter"),
            ("histogram", "Histogram"),
            ("summary", "Summary"),
        ],
        required=True,
        default="gauge",
    )
    model_id = fields.Many2one(
        "ir.model",
        required=True,
        ondelete="cascade",
    )
    model = fields.Char(
        string="Related Document Model",
        related="model_id.model",
        help="""Choose a model where the button is placed. You can find the
                model name in the URL. For example the model of this page is
                \'model=printnode.action.button\'.
                Check this in the URL after the \'model=\'.""",
    )
    domain = fields.Text(
        default="[]",
    )
    field_id = fields.Many2one(
        "ir.model.fields",
        "Measured Field",
        domain="""[('store', '=', True), ('model_id', '=', model_id),
            ('ttype', 'in', ['float','integer','monetary'])]""",
    )
    field = fields.Char(related="field_id.name")
    operation = fields.Selection(
        [
            ("sum", "Sum"),
            ("avg", "Average"),
            ("count", "Count"),
            ("min", "Min"),
            ("max", "Max"),
        ],
        default="sum",
    )

    @api.constrains("name")
    def _validate_name(self):
        for rec in self:
            if " " in rec.name:
                raise ValidationError(_("Metric name must not contain spaces."))
            if not str.islower(rec.name):
                raise ValidationError(_("Metric name must be lower case."))

    def _get_default_domain(self):
        if self.name == "odoo_cron_jobs_not_triggered":
            domain = [
                "&",
                (
                    "nextcall",
                    "<=",
                    (datetime.datetime.now() - datetime.timedelta(days=2)).strftime(
                        "%Y-%m-%d"
                    ),
                ),
                ("active", "=", True),
            ]
        elif self.name == "odoo_pending_mails":
            domain = [
                (
                    "date",
                    ">=",
                    (datetime.datetime.now() - datetime.timedelta(days=30)).strftime(
                        "%Y-%m-%d"
                    ),
                )
            ]
        else:
            domain = literal_eval(self.domain)
        return domain

    def _get_model_count(self):
        """Count model records."""
        self.ensure_one()
        related_model = self.env[self.model]
        domain = self._get_default_domain()
        return related_model.search_count(domain)

    def _get_field_value(self):
        """Run operation for selected field."""
        self.ensure_one()
        related_model = self.env[self.model]
        domain = self._get_default_domain()
        operation = self.operation
        if self.field_id:
            records = related_model.search(domain)
            values = records.mapped(self.field)
            if values:
                if operation == "avg":
                    return sum(values) / len(values)
                elif operation == "sum":
                    return sum(values)
                elif operation == "count":
                    return len(values)
                elif operation == "min":
                    return min(values)
                elif operation == "max":
                    return max(values)
            else:
                return 0
        else:
            return 0

    def _get_value(self):
        """Generic method to return metric value."""
        if self.field_id:
            return self._get_field_value()
        else:
            return self._get_model_count()
        
    ### ADDITIONAL METRICS FOR SYSTEM & ODOO MONITORING ###

    @staticmethod
    def get_system_metrics():
        """ Collect system-level metrics using psutil """
        ### Return System Metrics ####
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "cpu_usage_percentage": psutil.cpu_percent(interval=1),
            "memory_used_gb": mem.used / (1024 ** 3),  # Convert bytes to GB
            "memory_total_gb": mem.total / (1024 ** 3),  # Convert bytes to GB
            "disk_used_gb": disk.used / (1024 ** 3),
            "disk_total_gb": disk.total / (1024 ** 3),
            "memory_usage_percentage": (mem.used / mem.total) * 100,
            "disk_usage_percentage": (disk.used / disk.total) * 100,
        }

    @staticmethod
    def get_online_users():
        """ Count active users (logged in) """
        return request.env['bus.presence'].sudo().search_count([('status', '=', 'online')])
    
    @staticmethod
    def get_total_users():
        """ Count active users (logged in) """
        return request.env['bus.presence'].sudo().search_count([])

    @staticmethod
    def get_request_response_time():
        """ Calculate average request response time """
        logs = request.env['ir.logging'].sudo().search([
            ('name', '=', 'odoo.http'),
            ('type', '=', 'server'),
            ('level', '=', 'INFO')
        ], limit=50, order="create_date desc")

        response_times = [float(log.message.split()[-2]) for log in logs if "Request duration" in log.message]
        return sum(response_times) / len(response_times) if response_times else 0

    @staticmethod
    def get_query_execution_time():
        """ Extract query execution times from ir.logging """
        logs = request.env['ir.logging'].sudo().search([
            ('type', '=', 'sql'),
            ('level', '=', 'INFO')
        ], limit=50, order="create_date desc")

        execution_times = [float(log.message.split()[-2]) for log in logs if "executed in" in log.message]
        return sum(execution_times) / len(execution_times) if execution_times else 0