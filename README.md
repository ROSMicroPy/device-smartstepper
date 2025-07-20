# SmartStepper Module

A web-controlled stepper motor interface that integrates with the MotorControl library to provide a user-friendly web interface for controlling stepper motors.

## Features

- **Web Interface**: Modern, responsive web form for motor control
- **MotorControl Integration**: Uses the universal MotorControl library
- **Real-time Control**: Direct control of stepper motor direction, speed, and steps
- **Status Monitoring**: Real-time motor status and position tracking
- **Configurable**: Easy configuration through JSON files
- **RESTful API**: Clean API endpoints for integration

## Architecture

The SmartStepper module consists of:

1. **SmartStepper Class**: Main controller that integrates MotorControl with web server
2. **Web Interface**: JSON-based form layout served to the WebTester
3. **API Endpoints**: RESTful endpoints for motor control and status
4. **Configuration**: JSON-based configuration system

## Installation

1. Ensure you have the MotorControl library in the parent directory
2. Ensure you have the MicroPyServer library in the MicroPyServer directory
3. Install required Python dependencies:

```bash
pip install typing
```

## Usage

### Starting the Server

```python
from SmartStepper.src.SmartStepper import SmartStepper

# Create and start the server
stepper = SmartStepper(host="0.0.0.0", port=8080)
stepper.start()
```

Or run directly:

```bash
cd SmartStepper
python src/SmartStepper.py
```

### Web Interface

1. Start the SmartStepper server
2. Open the WebTester application
3. Enter the layout URL: `http://localhost:8080/api/layout`
4. Click "Load Layout" to load the motor control form
5. Initialize the motor using the API endpoint
6. Use the form to control the motor

### API Endpoints

#### GET /api/layout
Returns the JSON layout for the web form.

**Response:**
```json
{
  "title": "SmartStepper Control",
  "description": "Control your stepper motor with direction and speed settings",
  "submitUrl": "/api/control",
  "elements": [...]
}
```

#### POST /api/init
Initialize the stepper motor.

**Request Body:**
```json
{
  "step_pin": 18,
  "dir_pin": 19,
  "enable_pin": 20
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Stepper motor initialized successfully"
}
```

#### POST /api/control
Control the stepper motor.

**Request Body:**
```json
{
  "direction": "forward",
  "speed": 60,
  "steps": 200
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Motor moved 200 steps forward at 60 RPM",
  "position": 200
}
```

#### GET /api/status
Get current motor status.

**Response:**
```json
{
  "status": "initialized",
  "message": "Motor is ready",
  "position": 200,
  "speed": 60,
  "initialized": true
}
```

## Configuration

The module uses `config.json` for configuration:

```json
{
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
  }
}
```

## Web Form Features

The web interface provides:

- **Direction Control**: Forward/Backward selection
- **Speed Control**: RPM setting with validation
- **Step Control**: Number of steps to move
- **Real-time Feedback**: Status and position updates
- **Error Handling**: Clear error messages

## Integration with WebTester

The SmartStepper module is designed to work seamlessly with the WebTester application:

1. **Dynamic Form Loading**: The WebTester loads the form layout from `/api/layout`
2. **Form Submission**: User inputs are sent to `/api/control`
3. **Response Display**: Results are displayed in the WebTester interface
4. **Error Handling**: Errors are properly formatted and displayed

## Motor Control Features

- **Direction Control**: Forward and backward movement
- **Speed Control**: Adjustable RPM from 0-1000
- **Step Control**: Precise step-by-step movement
- **Position Tracking**: Real-time position monitoring
- **Safety Features**: Input validation and error handling

## Development

### Adding New Features

1. **New API Endpoints**: Add routes in `setup_routes()`
2. **Form Elements**: Modify the layout JSON in `get_layout()`
3. **Motor Functions**: Extend the SmartStepper class with new methods

### Testing

1. Start the SmartStepper server
2. Use the WebTester to test the interface
3. Test API endpoints directly with curl or Postman
4. Verify motor responses and error handling

## Troubleshooting

### Common Issues

1. **Motor Not Initialized**: Call `/api/init` first
2. **Import Errors**: Check MotorControl and MicroPyServer paths
3. **Port Conflicts**: Change port in config.json
4. **GPIO Errors**: Verify pin assignments and permissions

### Debug Mode

Enable debug output by modifying the SmartStepper class:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This module is part of the ROSMicroPy-Devices project and follows the same licensing terms. 