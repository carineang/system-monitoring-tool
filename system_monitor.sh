#!/bin/bash

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Check CPU usage
check_cpu_usage() {
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' | cut -d'.' -f1)
    echo "$cpu_usage"
}

log_message "Checking CPU usage..."
CPU_USAGE=$(get_cpu_usage)
echo "CPU Usage: ${CPU_USAGE}%"