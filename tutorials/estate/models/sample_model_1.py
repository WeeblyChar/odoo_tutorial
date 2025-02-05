from odoo import models, fields

class SampleEstateModel(models.Model):
    _name = "estate.property"
    _description = "test model for estate, why are there so many variables? what?"
    

    name = fields.Char('Estate Name', required=True)
    description = fields.Text('Estate Description', required=True)
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Date Availability', required=True, default=fields.Date.today)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', required=True)
    bedrooms = fields.Integer('Bedrooms', required=True, default=1)
    living_area = fields.Integer('Living Area (Square Meter)', required=True, default=0)
    facades = fields.Integer('Facades', default=1)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area (Square Meter)', default=0)
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='Please select the garden\'s orientation relative to the property.'
    )
    temp_check_update = fields.Boolean('Temp', default=False)
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The amount of price cannot be negative!'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The amount of price cannot be negative!'),
        ('check_living_area', 'CHECK(living_area >= 0)', 'The size of living area cannot be negative!'),
        ('check_garden_area', 'CHECK(garden_area >= 0)', 'The size of garden area cannot be negative!'),
        ('check_facades', 'CHECK(facades >= 0)', 'The amount of facades cannot be negative!'),
    ]