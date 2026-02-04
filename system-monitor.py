#!/usr/bin/env python3

import os
import sys
import json
import yaml
import psutil

def load_config(config_file="config.yaml"):
    print(f"Loading config from: {config_file}")

    if not os.path.exists(config_file):
        print("Config file not found.")
        sys.exit(1)

    try:
        with open(config_file, "r") as f:
            if config_file.endswith(".yaml"):
                config = yaml.safe_load(f)
            else:
                config = json.load(f)

        print("Config loaded successfully.")
        return config

    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)


def get_cpu_info():
    try:
        cpu_percentage = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_frequency = psutil.cpu_freq()
        
        return {
            'percent': cpu_percentage,
            'count': cpu_count,
            'frequency': cpu_frequency.current if cpu_frequency else None
        }
    
    except Exception as e:
        print(f"Error getting CPU info: {e}")
        return {'percent': 0, 'count': 0, 'frequency': None}
    
def get_memory_info():
    try:
        memory = psutil.virtual_memory()

        # Convert bytes to GB
        def bytes_to_gb(bytes_value):
            return bytes_value / (1024 ** 3)
        
        return {
            'total_gb': bytes_to_gb(memory.total),
            'used_gb': bytes_to_gb(memory.used),
            'percent': memory.percent
        }
    
    except Exception as e:
        print(f"Error getting memory info: {e}")
        return {'total_gb': 0, 'available_gb': 0, 'used_gb': 0, 'percent': 0}

def get_disk_info(path="/"):
    try:
        disk = psutil.disk_usage(path)
        
        # Convert bytes to GB
        def bytes_to_gb(bytes_value):
            return bytes_value / (1024 ** 3)
        
        return {
            'total_gb': bytes_to_gb(disk.total),
            'used_gb': bytes_to_gb(disk.used),
            'free_gb': bytes_to_gb(disk.free),
            'percent': disk.percent
        }
    except Exception as e:
        print(f"Error getting disk info: {e}")
        return {'total_gb': 0, 'used_gb': 0, 'free_gb': 0, 'percent': 0}


if __name__ == "__main__":
    config = load_config()
    print("\n=== Testing CPU Monitoring ===")
    cpu_info = get_cpu_info()
    print(f"CPU Usage: {cpu_info['percent']}%")
    print(f"CPU Cores: {cpu_info['count']}")
    if cpu_info['frequency']:
        print(f"CPU Frequency: {cpu_info['frequency']} MHz")
    
    # Check cpu threshold
    if cpu_info['percent'] > config['thresholds']['cpu']:
        print("ALERT: CPU threshold exceeded!")
    else:
        print("OK: CPU within normal range.")

    print("\n=== Testing Memory Monitoring ===")
    memory_info = get_memory_info()
    print(f"Memory Usage: {memory_info['percent']}%")
    print(f"Used: {memory_info['used_gb']:.2f} GB / {memory_info['total_gb']:.2f} GB")
    
    # Check memory threshold
    if memory_info['percent'] > config['thresholds']['memory']:
        print("ALERT: Memory threshold exceeded!")
    else:
        print("OK: Memory within normal range.")

    print("\n=== Testing Disk Monitoring ===")
    disk_info = get_disk_info("/")
    print(f"Disk Usage: {disk_info['percent']}%")
    print(f"Used: {disk_info['used_gb']:.2f} GB / {disk_info['total_gb']:.2f} GB")
    print(f"Free: {disk_info['free_gb']:.2f} GB")
    
    # Check disk threshold
    if disk_info['percent'] > config['thresholds']['disk']:
        print("ALERT: Disk threshold exceeded!")
    else:
        print("OK: Disk within normal range.")
