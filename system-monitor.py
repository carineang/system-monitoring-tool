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
    

if __name__ == "__main__":
    config = load_config()
    cpu_info = get_cpu_info()
    print("=== Testing CPU Monitoring ===")
    print(f"CPU Usage: {cpu_info['percent']}%")
    print(f"CPU Cores: {cpu_info['count']}")
    if cpu_info['frequency']:
        print(f"CPU Frequency: {cpu_info['frequency']} MHz")
    
    # Check cpu threshold
    if cpu_info['percent'] > config['thresholds']['cpu']:
        print("ALERT: CPU threshold exceeded!")
    else:
        print("OK: CPU within normal range.")
