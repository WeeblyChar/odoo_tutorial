{
    'name': "Odoo OpenTelemetry Integration",
    
    'summary': """
        Integrate Odoo with OpenTelemetry for logging, tracing, and metrics
    """,
    
    'description': """
        Integrate Odoo with OpenTelemetry for logging, tracing, and metrics
    """,
    
    'category': 'Tutorials/Odoo_OpenTelemetry_Integration',
    'installable': True,
    'application': True,
    'version': '1.0',
    'author': 'Salt',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3'
}
