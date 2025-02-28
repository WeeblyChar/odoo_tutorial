[![Build Status](https://runbot.odoo.com/runbot/badge/flat/1/master.svg)](https://runbot.odoo.com/runbot)
[![Tech Doc](https://img.shields.io/badge/master-docs-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/documentation/master)
[![Help](https://img.shields.io/badge/master-help-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](https://img.shields.io/badge/master-nightly-875A7B.svg?style=flat&colorA=8F8F8F)](https://nightly.odoo.com/)

Odoo
----

Modified Odoo with Open Telemetry LGTM brought to you via Open Telemetry Module wihtin the app itself.


To Do List:
- Connect Open Telemetry to its backends (Loki, Tempo, Grafana and Prometheus) and Odoo. (OK)
    -> Loki (OK)
        - Connect Odoo via OTel receiver. (OK)
        - Connect Grafana via OTel exporter. (OK)
        - Build a pipeline for the data to be transmitted. (OK)
        - Check if data is received in Grafana. (OK)
    -> Tempo (OK)
        - Connect Odoo via OTel receiver. (OK)
        - Connect Grafana via OTel exporter. (OK)
        - Build a pipeline for the data to be transmitted. (OK)
        - Check if data is received in Grafana. (OK)
    -> Prometheus (OK)
        - Connect Odoo via OTel receiver. (OK)
        - Connect Grafana via OTel exporter. (OK)
        - Build a pipeline for the data to be transmitted. (OK)
        - Check if data is received in Grafana. (OK)
- Check if data is valid. (DEV)
    -> Loki (BETA)
        - Data validation. (OK)
        - Export data from Line variable using regexp. (OK)
        - TBA
    -> Tempo (DEV)
        - Data validation. (?)
        - TBA
    -> Prometheus (DEV)
        - Data validation. (BAD)
        - Integrate Prometheus Exporter module. [https://github.com/Mint-System/Odoo-Apps-Server-Tools/tree/17.0/prometheus_exporter](Prometheus Exporter by Mint System). (OK)
        - Data validation. (OK)
        -> Custom metrics. (DEV)
            - ORM Metrics. (DEV)
            - System Metrics. (OK)

- Fix and prevent future problems where Prometheus Connection from Open Telemetry to Odoo is cut during a module installation.
- Create Dashboard. DEV