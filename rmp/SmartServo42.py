#!/usr/bin/env python3
"""
SmartServo42 Module

This module provides a web interface for controlling servo motors using the MotorControl library.
It inherits from SmartStepper and uses a servo-specific configuration file.
"""

from rmp.SmartStepper import SmartStepper


class SmartServo42(SmartStepper):
    """SmartServo42 controller with web interface, inheriting from SmartStepper."""
    
    def __init__(self, host="0.0.0.0", port=8080, config_file="servo42_config.json"):
        """Initialize SmartServo42 with servo-specific configuration."""
        # Call parent constructor with servo config file
        super().__init__(host=host, port=port, config_file=config_file)


def main():
    """Main function to run SmartServo42."""
    try:
        servo = SmartServo42()
        servo.start()
    except KeyboardInterrupt:
        print("\nShutting down SmartServo42...")
        try:
            servo.stop()
        except Exception as e:
            print(f"Error during shutdown: {e}")
    except Exception as e:
        print(f"Error in main: {e}")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main() 