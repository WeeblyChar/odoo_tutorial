{
    'name': "Odoo OpenTelemetry Integration",
    
    'summary': """
        Integrate Odoo with OpenTelemetry for logging, tracing, and metrics. Test Update 4.
    """,
    
    'description': """
        Integrate Odoo with OpenTelemetry for logging, tracing, and metrics. Test Update 4.
    """,
    
    'category': 'inDevModules/Odoo_OpenTelemetry_Integration',
    'installable': True,
    'application': True,
    'version': '1.0',
    'author': 'Amsal',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_otel_settings_views.xml',
        'views/odoo_otel_menu_views.xml',
    ],
    'external_dependencies':{
      'python': ['opentelemetry-distro', 'opentelemetry-exporter-otlp', 'opentelemetry-exporter-prometheus'],  
    },
    'license': 'AGPL-3'
}
