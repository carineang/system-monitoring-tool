## Linux System Monitoring Tool

A lightweight **Python-based Linux system monitoring tool** that tracks CPU, memory, and disk usage, with thresholds-based alerts and real-time logging.


## Features

| Feature | Description |
|---------|-------------|
| **Real-time Monitoring** | Track CPU, memory, and disk usage |
| **Multiple Modes** | One-time check or continuous monitoring |
| **Threshold-based Alerts** | Get notified when resources exceed limits |
| **Logging** | Real-time logs for one-time and daemon modes |


## Project Structure

```
.
├── system-monitor.py      # Main Python monitoring script
├── system-monitor.sh      # Bash launcher (daemon mode)
├── config.yaml            # Configuration file
├── requirements.txt       # Required dependencies
├── logs/                  # Log directory (auto-generated)
│   ├── monitor.log
│   └── alerts.log
└── README.md
```


## Requirements

- Python 3.11+
- psutil
- PyYAML


## Install Dependencies

```bash
pip install requirements.txt
```


## Configuration

Edit `config.yaml` to customize thresholds and monitoring behavior:

```yaml
thresholds:
  cpu: 80
  memory: 80
  disk: 80

monitoring:
  interval: 30
  log_level: "INFO"
```

### Thresholds

- `cpu` – Alert when CPU usage exceeds this percentage
- `memory` – Alert when memory usage exceeds this percentage
- `disk` – Alert when disk usage exceeds this percentage

### Monitoring

- `interval` – Time in seconds between checks (daemon mode)
- `log_level` – Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)


## Usage

### 1. One-Time System Check

Runs a one-time system resource check.

```bash
python3 system-monitor.py --check
```

### 2. Continuous Monitoring (Daemon Mode)

Runs continuously at configured interval.

```bash
python3 system-monitor.py --daemon
```

Or use the bash launcher:

```bash
chmod +x system-monitor.sh
./system-monitor.sh
```

Stop with:

```
Ctrl + C
```


## Alerts

When a threshold is exceeded:

- A red alert message is printed to the console
- A warning is logged in:
  - `logs/monitor.log`
  - `logs/alerts.log`

Example alert message:

```
ALERT [CPU]: CPU usage 92% > 80%
```


## Logging

Logs are stored in the `logs/` directory (auto-generated):

- `alerts.log`: Alert-specific entries
- `monitor.log`: General monitoring logs

Example log entry:

```
2026-03-12 09:56:52 - INFO - CPU: 28.3%
```
