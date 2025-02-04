from odoo import models, fields

class SampleEstateModel(models.Model):
    _name = "estate.property"
    _description = "test model for estate, why are there so many variables? what?"
    

    name = fields.Char('Estate Name', required=True)
    description = fields.Text('Estate Description', required=True)
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('date_availability', requred=True, default=fields.Date.today)
    expected_price = fields.Float('expected_price',required=True)
    selling_price = fields.Float('selling_price',required=True)
    bedrooms = fields.Integer('bedrooms', required=True)
    living_area = fields.Integer('living_area', default=0)
    facades = fields.Integer('facades', default=0)
    garage = fields.Boolean('garage', default=False)
    garden = fields.Boolean('garden', default=False)
    garden_area = fields.Integer('garden_area', default=0)
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='Please select the garden\'s orientation relative to the property.'
    )
    