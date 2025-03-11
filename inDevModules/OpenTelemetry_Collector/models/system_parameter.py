from odoo import models, fields, api

class SystemParameter(models.Model):
    _name = 'ir.system.parameter'
    _description = 'System Parameter'
    _rec_name = 'name'

    name = fields.Char(string='Parameter Name', required=True)
    value_ids = fields.One2many('ir.system.parameter.value', 'parameter_id', string='Values')
    value_display = fields.Text(string='Value', compute='_compute_value_display', store=True)

    @api.depends('value_ids.value')
    def _compute_value_display(self):
        for record in self:
            record.value_display = "\n".join(record.value_ids.mapped('value'))

class SystemParameterValue(models.Model):
    _name = 'ir.system.parameter.value'
    _description = 'System Parameter Value'

    parameter_id = fields.Many2one('ir.system.parameter', string='Parameter', required=True, ondelete='cascade')
    value = fields.Char(string='Value', required=True)