#!/bin/bash

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Check CPU usage
check_cpu_usage() {
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' | cut -d'.' -f1)
    echo "$cpu_usage"
}

# Check memory usage
check_memory_usage() {
    mem_info=$(free | grep Mem)
    total_mem=$(echo "$mem_info" | awk '{print $2}')
    used_mem=$(echo "$mem_info" | awk '{print $3}')
    mem_usage=$(( (used_mem * 100) / total_mem ))
    echo "$mem_usage"
}

log_message "Checking CPU usage..."
CPU_USAGE=$(check_cpu_usage)
echo "CPU Usage: ${CPU_USAGE}%"

log_message "Checking memory usage..."
MEMORY_USAGE=$(check_memory_usage)
echo "Memory Usage: ${MEMORY_USAGE}%"