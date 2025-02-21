{
    'name': 'Custom HTTP Tracing Module',
    'version': '1.0',
    'summary': 'Adds OpenTelemetry tracing for all HTTP requests',
    'description': 'Adds OpenTelemetry tracing for all HTTP requests',
    'author': 'Salt',
    'depends': ['base'],
    'data': [],
    'installable': True,
    'auto_install': True, # <-- Automatically install this package to start monitoring Odoo
    'category': 'inDevModules/Custom_Tracing',
    'external_dependencies':{
      'python': ['opentelemetry-distro', 'opentelemetry-exporter-otlp'],  
    },
    'license': 'AGPL-3',
}
