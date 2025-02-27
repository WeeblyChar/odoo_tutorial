{
    'name': 'Open Telemetry Monitoring Module',
    'version': '1.0',
    'summary': 'Integrates custom Open Telemetry configuration for Odoo',
    'description': """
                    Integrates custom Open Telemetry configuration for Odoo.
                    This module uses Grafana Loki (logs), Grafana Tempo (trace/span), Prometheus (metrics) and Grafana (Visualization).
                    People call it OTel-LGTM, how to memorize it? Just follow this phrase, \"this OpenTelemetry Looks Good To Me (OTel-LGTM)\".
                    Sounds like a joke but I did that too many times and it works. Jokes aside, there will be an extension for metrics in this module
                    that you can access using Developer Mode. Go to Settings -> Technical -> Metrics (most likely at the bottom most list).
                   """,
    'author': 'Amsal',
    'depends': ['base', 'resource'],
    'data': [],
    'installable': True,
    'application': False, # <-- No, this is not an application. It's just an extension.
    'auto_install': False, # <-- Automatically install this package to start monitoring Odoo during server start (optional)
    'category': 'inDevModules/Custom_Tracing',
    "data": [
        "security/ir.model.access.csv",
        "data/ir_metric.xml",
        "views/ir_metric.xml",
    ],
    'external_dependencies':{
      'python': [ # <-- Refer to Dockerfile if module breaks
        'opentelemetry-distro',
        'opentelemetry-exporter-otlp',
        'prometheus_client'
      ],  
    },
    'license': 'AGPL-3',
}
