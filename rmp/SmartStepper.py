#!/usr/bin/env python3
"""
SmartStepper Module

This module provides a web interface for controlling stepper motors using the MotorControl library.
It includes a JSON profile for the web form and endpoint interface for motor control.
"""

import json
import sys
import os
from typing import Dict, Any, Optional


# Add MotorControl to path
motorcontrol_path = os.path.join(os.path.dirname(__file__), '..', '..', 'MotorControl')
sys.path.append(motorcontrol_path)
sys.path.append(os.path.join(motorcontrol_path, 'ai'))
from motorControl import MotorController, MotorType

# Add MicroPyServer to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'MicroPyServer'))
from src.micropyserver import MicroPyServer


class SmartStepper:
    """SmartStepper controller with web interface."""
    
    def __init__(self, host="0.0.0.0", port=8080, config_file=None):
        """Initialize SmartStepper with web server."""
        self.config = self._load_config(config_file)
        self.server = MicroPyServer(host=host, port=port)
        self.motor_controller = MotorController()
        self.stepper_motor = None
        self.setup_routes()
    
    def _load_config(self, config_file=None):
        """Load configuration from JSON file."""
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
        
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
                },
                "default_settings": {
                    "microsteps": 1,
                    "default_speed": 60,
                    "default_steps": 200
                }
            },
            "web_interface": {
                "title": "SmartStepper Control",
                "description": "Control your stepper motor with direction and speed settings",
                "speed_range": {
                    "min": 0,
                    "max": 1000
                },
                "steps_range": {
                    "min": 1,
                    "max": 10000
                }
            }
        }
    
    def setup_routes(self):
        """Setup HTTP routes for the web interface."""
        # Serve the layout JSON
        self.server.add_route("/api/layout", self.get_layout, "GET")
        
        # Handle motor control commands
        self.server.add_route("/api/control", self.control_motor, "POST")
        
        # Get motor status
        self.server.add_route("/api/status", self.get_status, "GET")
        
        # Initialize motor
        self.server.add_route("/api/init", self.initialize_motor, "POST")
    
    def get_layout(self, request):
        """Return the JSON layout for the web form."""
        web_config = self.config.get('web_interface', {})
        motor_config = self.config.get('motor', {})
        
        layout = {
            "title": web_config.get('title', 'SmartStepper Control'),
            "description": web_config.get('description', 'Control your stepper motor with direction and speed settings'),
            "submitUrl": "/api/control",
            "elements": [
                {
                    "id": "direction",
                    "type": "select",
                    "label": "Direction",
                    "options": [
                        {"value": "forward", "label": "Forward"},
                        {"value": "backward", "label": "Backward"}
                    ],
                    "defaultValue": "forward",
                    "required": True
                },
                {
                    "id": "speed",
                    "type": "input",
                    "inputType": "number",
                    "label": "Speed (RPM)",
                    "placeholder": "Enter speed in RPM",
                    "min": web_config.get('speed_range', {}).get('min', 0),
                    "max": web_config.get('speed_range', {}).get('max', 1000),
                    "defaultValue": str(motor_config.get('default_settings', {}).get('default_speed', 60)),
                    "required": True
                },
                {
                    "id": "steps",
                    "type": "input",
                    "inputType": "number",
                    "label": "Steps",
                    "placeholder": "Number of steps to move",
                    "min": web_config.get('steps_range', {}).get('min', 1),
                    "max": web_config.get('steps_range', {}).get('max', 10000),
                    "defaultValue": str(motor_config.get('default_settings', {}).get('default_steps', 200)),
                    "required": True
                },
                {
                    "id": "submit",
                    "type": "button",
                    "label": "Move Motor",
                    "action": "submit",
                    "style": "primary"
                },
                {
                    "id": "stop",
                    "type": "button",
                    "label": "Stop Motor",
                    "action": "custom",
                    "style": "danger"
                }
            ],
            "outputMappings": [
                {
                    "elementId": "status",
                    "responseKey": "status"
                },
                {
                    "elementId": "message",
                    "responseKey": "message"
                }
            ]
        }
        
        self.server.send("HTTP/1.1 200 OK\r\n")
        self.server.send("Content-Type: application/json\r\n")
        self.server.send("Access-Control-Allow-Origin: *\r\n")
        self.server.send("Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n")
        self.server.send("Access-Control-Allow-Headers: Content-Type\r\n")
        self.server.send("\r\n")
        self.server.send(json.dumps(layout))
    
    def control_motor(self, request):
        """Handle motor control commands."""
        try:
            # Parse request body
            body = self._get_request_body(request)
            data = json.loads(body) if body else {}
            
            direction = data.get('direction', 'forward')
            speed = float(data.get('speed', 60))
            steps = int(data.get('steps', 200))
            
            if not self.stepper_motor:
                response = {
                    "status": "error",
                    "message": "Motor not initialized. Please initialize first."
                }
            else:
                # Set direction (True for forward, False for backward)
                motor_direction = direction.lower() == 'forward'
                
                # Set speed
                self.stepper_motor.set_speed(speed)
                
                # Move motor
                success = self.stepper_motor.move_steps(steps, motor_direction)
                
                if success:
                    response = {
                        "status": "success",
                        "message": f"Motor moved {steps} steps {direction} at {speed} RPM",
                        "position": self.stepper_motor.get_stepper_position()
                    }
                else:
                    response = {
                        "status": "error",
                        "message": "Failed to move motor"
                    }
            
        except Exception as e:
            response = {
                "status": "error",
                "message": f"Error controlling motor: {str(e)}"
            }
        
        self.server.send("HTTP/1.1 200 OK\r\n")
        self.server.send("Content-Type: application/json\r\n")
        self.server.send("Access-Control-Allow-Origin: *\r\n")
        self.server.send("\r\n")
        self.server.send(json.dumps(response))
    
    def get_status(self, request):
        """Get current motor status."""
        if not self.stepper_motor:
            status = {
                "status": "not_initialized",
                "message": "Motor not initialized"
            }
        else:
            motor_status = self.stepper_motor.get_status()
            status = {
                "status": "initialized",
                "message": "Motor is ready",
                "position": motor_status.get("position", 0),
                "speed": motor_status.get("speed", 0),
                "initialized": motor_status.get("initialized", False)
            }
        
        self.server.send("HTTP/1.1 200 OK\r\n")
        self.server.send("Content-Type: application/json\r\n")
        self.server.send("Access-Control-Allow-Origin: *\r\n")
        self.server.send("\r\n")
        self.server.send(json.dumps(status))
    
    def initialize_motor(self, request):
        """Initialize the stepper motor."""
        try:
            # Parse request body
            body = self._get_request_body(request)
            data = json.loads(body) if body else {}
            
            # Get default pins from config
            default_pins = self.config.get('motor', {}).get('default_pins', {})
            default_settings = self.config.get('motor', {}).get('default_settings', {})
            
            # Use request data or fall back to config defaults
            step_pin = data.get('step_pin', default_pins.get('step_pin', 18))
            dir_pin = data.get('dir_pin', default_pins.get('dir_pin', 19))
            enable_pin = data.get('enable_pin', default_pins.get('enable_pin', 20))
            microsteps = data.get('microsteps', default_settings.get('microsteps', 1))
            
            # Create stepper motor
            self.stepper_motor = self.motor_controller.create_motor(
                "smart_stepper",
                MotorType.STEPPER,
                "example_stepper_driver",
                step_pin=step_pin,
                dir_pin=dir_pin,
                enable_pin=enable_pin,
                microsteps=microsteps
            )
            
            # Initialize the motor
            success = self.stepper_motor.initialize()
            
            if success:
                response = {
                    "status": "success",
                    "message": f"Stepper motor initialized successfully with pins: step={step_pin}, dir={dir_pin}, enable={enable_pin}"
                }
            else:
                response = {
                    "status": "error",
                    "message": "Failed to initialize stepper motor"
                }
                
        except Exception as e:
            response = {
                "status": "error",
                "message": f"Error initializing motor: {str(e)}"
            }
        
        self.server.send("HTTP/1.1 200 OK\r\n")
        self.server.send("Content-Type: application/json\r\n")
        self.server.send("Access-Control-Allow-Origin: *\r\n")
        self.server.send("\r\n")
        self.server.send(json.dumps(response))
    
    def _get_request_body(self, request):
        """Extract request body from HTTP request."""
        lines = request.split('\r\n')
        body_start = False
        body = ""
        
        for line in lines:
            if body_start:
                body += line
            elif line == "":
                body_start = True
        
        return body
    
    def start(self):
        """Start the SmartStepper web server."""
        print("Starting SmartStepper web server...")
        print("Web interface available at: http://localhost:8080")
        print("API endpoints:")
        print("  GET  /api/layout    - Get form layout")
        print("  POST /api/init      - Initialize motor")
        print("  POST /api/control   - Control motor")
        print("  GET  /api/status    - Get motor status")
        self.server.start()
    
    def stop(self):
        """Stop the SmartStepper web server."""
        if self.stepper_motor:
            self.stepper_motor.shutdown()
        self.server.stop()


def main():
    """Main function to run SmartStepper."""
    stepper = SmartStepper()
    try:
        stepper.start()
    except KeyboardInterrupt:
        print("\nShutting down SmartStepper...")
        stepper.stop()


if __name__ == "__main__":
    main()
