#!/usr/bin/env python3
"""
SmartStepper Startup Script

This script provides an easy way to start the SmartStepper server with various options.
"""

import sys
import os
import argparse
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from SmartStepper import SmartStepper


def load_config():
    """Load configuration from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "server": {
                "host": "0.0.0.0",
                "port": 8080
            },
            "motor": {
                "default_pins": {
                    "step_pin": 18,
                    "dir_pin": 19,
                    "enable_pin": 20
                }
            }
        }


def main():
    """Main function to start SmartStepper with command line options."""
    parser = argparse.ArgumentParser(description='SmartStepper Web Interface')
    parser.add_argument('--host', type=str, help='Host address to bind to')
    parser.add_argument('--port', type=int, help='Port to listen on')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--test', action='store_true', help='Run tests instead of starting server')
    
    args = parser.parse_args()
    
    if args.test:
        # Run tests
        print("Running SmartStepper tests...")
        test_script = os.path.join(os.path.dirname(__file__), 'test_smartstepper.py')
        if os.path.exists(test_script):
            os.system(f'python {test_script}')
        else:
            print("Test script not found!")
        return
    
    # Load configuration
    config = load_config()
    
    # Override with command line arguments
    host = args.host or config['server']['host']
    port = args.port or config['server']['port']
    
    print("=" * 50)
    print("SmartStepper Web Interface")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print("=" * 50)
    print()
    print("Web Interface URLs:")
    print(f"  Layout: http://{host}:{port}/api/layout")
    print(f"  Status: http://{host}:{port}/api/status")
    print()
    print("API Endpoints:")
    print(f"  GET  /api/layout    - Get form layout")
    print(f"  POST /api/init      - Initialize motor")
    print(f"  POST /api/control   - Control motor")
    print(f"  GET  /api/status    - Get motor status")
    print()
    print("To use with WebTester:")
    print(f"1. Open WebTester application")
    print(f"2. Enter layout URL: http://{host}:{port}/api/layout")
    print(f"3. Click 'Load Layout'")
    print(f"4. Initialize motor and start controlling!")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Create and start SmartStepper
    stepper = SmartStepper(host=host, port=port)
    
    try:
        stepper.start()
    except KeyboardInterrupt:
        print("\nShutting down SmartStepper...")
        stepper.stop()
        print("Goodbye!")


if __name__ == "__main__":
    main() 