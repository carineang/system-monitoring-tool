# Linux System Monitoring Tool

A lightweight Python-based Linux system monitoring tool that monitors CPU, memory, and disk usage, supports configurable threshold-based alerts, and provides real-time logging. The application can be run directly with Python or deployed in a Docker container for consistent and portable execution.

## Features

| Feature | Description |
|---------|-------------|
| **Real-time Monitoring** | Track CPU, memory, and disk usage |
| **Multiple Modes** | One-time check or continuous monitoring |
| **Threshold-based Alerts** | Get notified when resources exceed limits |
| **Logging** | Real-time logs for one-time and daemon modes |
| **Docker Support** | Containerized deployment using Docker and Docker Compose |

## Project Structure

```
├── system-monitor.py      # Main Python monitoring script
├── system-monitor.sh      # Bash launcher (Daemon mode)
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore rules
├── logs/                  # Log directory (auto-generated)
│   ├── monitor.log
│   └── alerts.log
└── README.md

```

## Requirements

### Running Locally

* Python 3.11+
* pip

### Running with Docker

* Docker Desktop (Windows/macOS)
* Docker Engine + Docker Compose (Linux)

## Installation

Clone the repository:

```bash
git clone https://github.com/carineang/system-monitoring-tool/
cd system-monitoring-tool
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Customize monitoring behavior by editing `config.yaml`.

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

### One-Time System Check

Run a single system resource check.

```bash
python3 system-monitor.py --check
```

## Continuous Monitoring

Run continuous monitoring using Python.

```bash
python3 system-monitor.py --daemon
```

Or use the Bash launcher.

```bash
chmod +x system-monitor.sh
./system-monitor.sh
```

Stop monitoring with:

```text
Ctrl + C
```

## Docker Deployment

### Build the Docker Image

```bash
docker build -t system-monitor .
```

### Docker Compose

Start the application:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

Rebuild after code changes:

```bash
docker compose up --build -d
```

## Alerts

When a threshold is exceeded:

* An alert is printed to the console.
* A warning entry is written to:
  * `logs/monitor.log`
  * `logs/alerts.log`

Example:

```text
ALERT [CPU]: CPU usage 92% > 80%
```

## Logging

Logs are stored in the `logs/` directory (auto-generated):

- `alerts.log`: Alert-specific entries
- `monitor.log`: General monitoring logs

Example:
```text
2026-03-12 09:56:52 - INFO - CPU: 28.3%
```

## Technologies Used

* Python 3.11
* psutil
* PyYAML
* Docker
* Docker Compose
