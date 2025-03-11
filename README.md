# Odoo with OpenTelemetry  

This is a modified version of Odoo with OpenTelemetry LGTM, integrated via the OpenTelemetry module within the application itself.  

## Access URLs  

- **Odoo:** [http://localhost:8069](http://localhost:8069)  
- **Grafana:** [http://localhost:3000](http://localhost:3000)  
- **Prometheus:** [http://localhost:9090](http://localhost:9090)  

## To-Do List  

### ✅ OpenTelemetry Integration with Backends  
- **Loki** ✅  
  - Connect Odoo via OpenTelemetry receiver. ✅  
  - Connect Grafana via OpenTelemetry exporter. ✅  
  - Build a pipeline for data transmission. ✅  
  - Verify data reception in Grafana. ✅  

- **Tempo** ✅  
  - Connect Odoo via OpenTelemetry receiver. ✅  
  - Connect Grafana via OpenTelemetry exporter. ✅  
  - Build a pipeline for data transmission. ✅  
  - Verify data reception in Grafana. ✅  

- **Prometheus** ✅  
  - Connect Odoo via OpenTelemetry receiver. ✅  
  - Connect Grafana via OpenTelemetry exporter. ✅  
  - Build a pipeline for data transmission. ✅  
  - Verify data reception in Grafana. ✅  

### 🔧 Data Validation (In Progress)  
- **Loki** (BETA)  
  - Validate logs. ✅  
  - Extract data from the `Line` variable using regex. ✅  
  - Further improvements (TBA).  

- **Tempo** (DEV)  
  - Validate traces. ❓  
  - Further improvements (TBA).  

- **Prometheus** (DEV)  
  - Validate metrics. ❌ (Issues found)  
  - Integrate Prometheus Exporter module: [Prometheus Exporter by Mint System](https://github.com/Mint-System/Odoo-Apps-Server-Tools/tree/17.0/prometheus_exporter) ✅  
  - Validate metrics after exporter module integration. ✅  
  - **Custom metrics:** (DEV)  
    - ORM Metrics (In Development)  
    - System Metrics ✅  

### 🛠 Fixes & Improvements  
- Resolve Prometheus connection issues between OpenTelemetry and Odoo during module installation.  
- Create a Grafana dashboard. (In Development)  
- Add detailed code documentation and explanations.  

*→ README design generated using ChatGPT*