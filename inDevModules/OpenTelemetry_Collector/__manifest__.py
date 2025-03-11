{
    'name': 'Open Telemetry Monitoring Module (Prototype Phase)',
    'version': '1.0',
    'summary': 'Integrates Custom Open Telemetry Configuration for Odoo.',
    'description': """
                    Integrates custom Open Telemetry configuration for Odoo.
                    This module uses Grafana Loki (logs), Grafana Tempo (trace/span), Prometheus (metrics) and Grafana (Visualization).
                    People call it OTel-LGTM, what does it mean? OTel (Open Telemetry) LGTM (Loki, Grafana, Tempo, Mimir).
                    Mimir is basically Prometheus so don\'t think too much about it.
                    How to memorize it? Just follow this phrase, \"this OpenTelemetry Looks Good To Me (OTel-LGTM)\".
                    Jokes aside, there will be an extension for metrics in this module.
                    You can access this by going into Developer Mode and go to Settings -> Technical -> Metrics. It should be listed under Resources.
                   """,
    'author': 'Amsal Anugrah',
    'depends': ['base', 'resource', 'bus'],
    'data': [],
    'installable': True,
    'application': False, # <-- No, this is not an application. It's just an extension.
    'auto_install': True, # <-- Automatically install this package to start monitoring Odoo during server start (optional)
    'category': 'inDevModules/OpenTelemetry_Collector',
    "data": [
        "views/ir_metric.xml",
        'views/system_parameter.xml',
        "security/ir.model.access.csv",
        "data/ir_metric.xml",
        'data/system_parameter.xml',
    ],
    'external_dependencies':{
      'python': [ # <-- Refer to Dockerfile if module breaks
        'opentelemetry-distro',
        'opentelemetry-exporter-otlp',
        'opentelemetry-instrumentation-psycopg2',
        'prometheus_client',
      ],
    },
    'license': 'AGPL-3',
}
