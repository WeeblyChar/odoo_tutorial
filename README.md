[![Build Status](https://runbot.odoo.com/runbot/badge/flat/1/master.svg)](https://runbot.odoo.com/runbot)
[![Tech Doc](https://img.shields.io/badge/master-docs-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/documentation/master)
[![Help](https://img.shields.io/badge/master-help-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](https://img.shields.io/badge/master-nightly-875A7B.svg?style=flat&colorA=8F8F8F)](https://nightly.odoo.com/)

# Odoo  

Modified Odoo with OpenTelemetry LGTM, integrated via the OpenTelemetry module within the app itself.  

## To-Do List  

### ✅ Connect OpenTelemetry to its backends (Loki, Tempo, Grafana, and Prometheus) and Odoo  
- **Loki** ✅  
  - Connect Odoo via OTel receiver. ✅  
  - Connect Grafana via OTel exporter. ✅  
  - Build a pipeline for data transmission. ✅  
  - Verify data reception in Grafana. ✅  

- **Tempo** ✅  
  - Connect Odoo via OTel receiver. ✅  
  - Connect Grafana via OTel exporter. ✅  
  - Build a pipeline for data transmission. ✅  
  - Verify data reception in Grafana. ✅  

- **Prometheus** ✅  
  - Connect Odoo via OTel receiver. ✅  
  - Connect Grafana via OTel exporter. ✅  
  - Build a pipeline for data transmission. ✅  
  - Verify data reception in Grafana. ✅  

### 🔧 Validate Data (In Progress)  
- **Loki** (BETA)  
  - Data validation. ✅  
  - Export data from the `Line` variable using regex. ✅  
  - TBA  

- **Tempo** (DEV)  
  - Data validation. ❓  
  - TBA  

- **Prometheus** (DEV)  
  - Data validation. ❌ (BAD)  
  - Integrate Prometheus Exporter module: [Prometheus Exporter by Mint System](https://github.com/Mint-System/Odoo-Apps-Server-Tools/tree/17.0/prometheus_exporter) ✅  
  - Data validation. ✅  
  - **Custom metrics:** (DEV)  
    - ORM Metrics. (DEV)  
    - System Metrics. ✅  

### 🛠 Fix Issues & Improvements  
- Prevent Prometheus connection loss from OpenTelemetry to Odoo during module installation.  
- Create Grafana Dashboard. (DEV)  