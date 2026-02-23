#!/usr/bin/env python3

import os
import sys
import json
import yaml
import psutil
import argparse
import logging
import time
from datetime import datetime

def setup_logging(log_level="INFO", log_file="monitor.log"):
    log_directory = "logs"
   
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    log_path = os.path.join(log_directory, log_file)
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    # Configure logging
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_path)
        ]
    )
    
    return logging.getLogger(__name__)

def send_alert(alert_type, message, config):
    logger = logging.getLogger(__name__)
    
    # Log the alert
    logger.warning(f"ALERT [{alert_type.upper()}]: {message}")
    
    alert_directory = "logs"
    if not os.path.exists(alert_directory):
        os.makedirs(alert_directory)
    
    alert_log = os.path.join(alert_directory, "alerts.log")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with open(alert_log, 'a') as f:
            f.write(f"[{timestamp}] {alert_type.upper()}: {message}\n")
    except Exception as e:
        logger.error(f"Failed to write alert to file: {e}")
    
    print(f"\033[91mALERT [{alert_type.upper()}]: {message}\033[0m")
    
    return True

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

def parse_arguments():
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False, usage="python3 system-monitor.py [--check | --daemon]")
    parser.add_argument("--check", action="store_true", help="Run one-time system check")
    parser.add_argument("--daemon", action="store_true", help="Run continuous system monitoring")
    return parser

def monitor_check(config):
    logger = logging.getLogger(__name__)
    logger.info("Running one-time system check.")
    print("\n" + "=" * 50)
    print("Running one-time system check.")

    # CPU Monitoring
    print("\n=== Start CPU Monitoring ===")    
    cpu_info = get_cpu_info()
    logger.info(f"CPU: {cpu_info['percent']}%")
    print(f"CPU Usage: {cpu_info['percent']}%")
    print(f"CPU Cores: {cpu_info['count']}")
    if cpu_info.get('frequency'):
        print(f"CPU Frequency: {cpu_info['frequency']} MHz")

    # Check CPU threshold
    if cpu_info['percent'] > config['thresholds']['cpu']:
        msg = f"CPU usage {cpu_info['percent']}% > {config['thresholds']['cpu']}%"
        send_alert('cpu', msg, config)
    else:
        print("\033[92mOK: CPU within normal range.\033[0m")

    # Memory Monitoring
    print("\n=== Start Memory Monitoring ===")
    memory_info = get_memory_info()
    logger.info(f"Memory: {memory_info['percent']}%")
    print(f"Memory Usage: {memory_info['percent']}%")
    print(f"Used: {memory_info['used_gb']:.2f} GB / {memory_info['total_gb']:.2f} GB")

    # Check memory threshold
    if memory_info['percent'] > config['thresholds']['memory']:
        msg = f"Memory usage {memory_info['percent']}% > {config['thresholds']['memory']}%"
        send_alert('memory', msg, config)
    else:
        print("\033[92mOK: Memory within normal range.\033[0m")

    # Disk Monitoring
    print("\n=== Start Disk Monitoring ===")
    disk_info = get_disk_info("/")
    logger.info(f"Disk: {disk_info['percent']}%")
    print(f"Disk Usage: {disk_info['percent']}%")
    print(f"Used: {disk_info['used_gb']:.2f} GB / {disk_info['total_gb']:.2f} GB")
    print(f"Free: {disk_info['free_gb']:.2f} GB")

    # Check disk threshold
    if disk_info['percent'] > config['thresholds']['disk']:
        msg = f"Disk usage {disk_info['percent']}% > {config['thresholds']['disk']}%"
        send_alert('disk', msg, config)
    else:
        print("\033[92mOK: Disk within normal range.\033[0m")
    
    print("\n" + "One-time system check completed.")
    print("=" * 50)
    logger.info("One-time system check completed.")
    

def monitor_daemon(config):
    logger = logging.getLogger(__name__)
    interval = config.get('monitoring', {}).get('interval', 60)
    
    logger.info(f"Run continuous monitoring. (interval: {interval}s)")
    print(f"Run continuous monitoring. (interval: {interval}s)")
    print("Press Ctrl+C to stop.")
    print("\n" + "=" * 50)
    
    try:
        cycle = 0
        while True:
            cycle += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"======== Monitoring cycle {cycle} started ========")
            print(f"[{timestamp}] Cycle {cycle}")
            
            # Get metrics
            cpu_info = get_cpu_info()
            memory_info = get_memory_info()
            disk_info = get_disk_info()
            
            # Display current percentage values
            print(f"CPU Usage: {cpu_info['percent']}%")
            print(f"Memory Usage: {memory_info['percent']}%")
            print(f"Disk Usage: {disk_info['percent']}%")

            logger.info(f"CPU: {cpu_info['percent']}%")
            logger.info(f"Memory: {memory_info['percent']}%")
            logger.info(f"Disk: {disk_info['percent']}%")
            
            # Check thresholds and send alerts
            alerts = []
            
            if cpu_info['percent'] > config['thresholds']['cpu']:
                msg = f"CPU usage {cpu_info['percent']}% > {config['thresholds']['cpu']}%"
                alerts.append(('cpu', msg))
                send_alert('cpu', msg, config)
            
            if memory_info['percent'] > config['thresholds']['memory']:
                msg = f"Memory usage {memory_info['percent']}% > {config['thresholds']['memory']}%"
                alerts.append(('memory', msg))
                send_alert('memory', msg, config)
            
            if disk_info['percent'] > config['thresholds']['disk']:
                msg = f"Disk usage {disk_info['percent']}% > {config['thresholds']['disk']}%"
                alerts.append(('disk', msg))
                send_alert('disk', msg, config)
            
            if alerts:
                print(f"\n\033[91m{len(alerts)} ALERT(S) TRIGGERED!\033[0m")
                logger.info(f"Alerts triggered: {len(alerts)}")
            else:
                logger.info("All systems are normal.")
                print("\033[92mOK: All systems are normal.\033[0m")
            
            print("=" * 50)
            logger.info(f"Cycle {cycle} completed, sleeping for {interval}s")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user.")
        print("\n\nMonitoring stopped by user.")
    except Exception as e:
        logger.error(f"Error in monitoring loop: {e}")
        print(f"\nError: {e}")


if __name__ == "__main__":
    parser = parse_arguments()
    args = parser.parse_args()

    config = load_config()
    
    log_level = config.get('monitoring', {}).get('log_level', 'INFO')
    logger = setup_logging(log_level)
    
    logger.info("=" * 50)
    logger.info("System Monitor Started.")
    logger.info(f"Log level: {log_level}")

    if args.check:
        monitor_check(config)

    elif args.daemon:
        monitor_daemon(config)

    else:
        parser.print_help()
