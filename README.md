# Python FIWARE Examples

Several examples using Python with FIWARE. The scripts cover the full lifecycle of a FIWARE-based IoT platform: entity management with Orion Context Broker, IoT Agent integration over HTTP and MQTT, historical data persistence, time series, and visualisation.

Some examples are based on the original curl-based [FIWARE tutorials](https://fiware-tutorials.readthedocs.io/en/latest/).

---

## Prerequisites

- Python 3.7+
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) to run the FIWARE stack locally
- `requests` and `paho-mqtt` Python libraries:

```bash
pip install requests paho-mqtt
```

---

## Configuration

All scripts read connection settings from a shared `settings.py` file. Copy the provided template and fill in your values:

```bash
cp settings-example.py settings.py
```

Then edit `settings.py`:

```python
USER = "your_username"
PASSWORD = "your_password"
SERVICE = "your_service"
SERVICE_PATH = "/your_service_path"
ORION_HOST = "your_orion_ip"
```

The `settings.py` file is listed in `.gitignore` and will not be committed to the repository.

---

## Running the FIWARE Stack Locally

The `docker/` folder contains Docker Compose files to spin up the required FIWARE components. Start the stack before running any script:

```bash
cd docker
docker compose up -d
```

---

## Examples

Scripts are numbered to indicate a suggested learning order. Each group covers a specific FIWARE component or topic.

| Prefix | Topic |
|---|---|
| 01 | Create entities in Orion Context Broker |
| 02 | Query entities |
| 03 | Update attributes |
| 04 | Delete entities |
| 05 | Subscriptions |
| 06–07 | Attribute updates and subscription cleanup |
| 08–09 | IoT Agent — Ultralight 2.0 over HTTP (provisioning, device simulation, commands) |
| 10 | IoT Agent — JSON protocol over HTTP |
| 11 | IoT Agent — Ultralight 2.0 over MQTT |
| 12 | IoT Agent — JSON protocol over MQTT |
| 13 | IoT Agent — attribute transformation |
| 14 | IoT Agent — multi-entity mapping |
| 15–16 | Cygnus and STH-Comet (historical data persistence and queries) |
| 17 | QuantumLeap and CrateDB (time series) |
| 18 | Apache Spark integration |
| 19 | WireCloud visualisation |
| 20 | Perseo — Complex Event Processing and rule-based alerting |

Within each group, scripts are suffixed with a step number (e.g. `08agent_device_ultralight1_provisioning`, `08agent_device_ultralight2_simdevice`, `08agent_device_ultralight3_sendcommand`) to indicate the order in which they should be run.

---

## Hardware Examples

The following folders contain MicroPython code for physical devices:

| Folder | Description |
|---|---|
| `esp32_connect_orion/` | Register an ESP32 as an entity in Orion |
| `esp32_update_attribute/` | Update an attribute from an ESP32 |
| `nodemcu_connect_orion/` | Register a NodeMCU as an entity in Orion |
| `nodemcu_device/` | Basic NodeMCU device example |
| `nodemcu_mqtt_device_fiware/` | NodeMCU device communicating via MQTT with FIWARE |

---

## Resources

- [FIWARE tutorials](https://fiware-tutorials.readthedocs.io/en/latest/)
- [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/)
- [IoT Agent for Ultralight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/)
- [IoT Agent for JSON](https://fiware-iotagent-json.readthedocs.io/en/latest/)
- [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/)
- [STH-Comet](https://fiware-sth-comet.readthedocs.io/en/latest/)
- [QuantumLeap](https://quantumleap.readthedocs.io/en/latest/)
- [Perseo](https://fiware-perseo-fe.readthedocs.io/en/latest/)
- [WireCloud](https://wirecloud.readthedocs.io/en/stable/)

---

## Author

**dgarridouma** · [GitHub](https://github.com/dgarridouma)
