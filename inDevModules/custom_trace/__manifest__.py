{
    'name': 'Custom HTTP Tracing Module',
    'version': '1.0',
    'summary': 'Adds OpenTelemetry tracing for all HTTP requests',
    'description': 'Adds OpenTelemetry tracing for all HTTP requests',
    'author': 'Salt',
    'depends': ['base', 'resource'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False, # <-- Automatically install this package to start monitoring Odoo
    'category': 'inDevModules/Custom_Tracing',
    "data": [
        "security/ir.model.access.csv",
        "data/ir_metric.xml",
        "views/ir_metric.xml",
    ],
    'external_dependencies':{
      'python': ['opentelemetry-distro', 'opentelemetry-exporter-otlp', 'prometheus_client'],  
    },
    'license': 'AGPL-3',
}
