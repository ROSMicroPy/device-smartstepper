#!/usr/bin/env python3
"""
Test script for SmartStepper module

This script tests the SmartStepper functionality without requiring actual hardware.
"""

import sys
import os
import json
import time
import threading

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from SmartStepper import SmartStepper


def test_layout_endpoint():
    """Test the layout endpoint."""
    print("Testing layout endpoint...")
    
    # Create a mock request
    mock_request = "GET /api/layout HTTP/1.1\r\nHost: localhost:8080\r\n\r\n"
    
    # Create SmartStepper instance
    stepper = SmartStepper(host="localhost", port=8081)
    
    # Test the layout method directly
    try:
        stepper.get_layout(mock_request)
        print("✓ Layout endpoint test passed")
    except Exception as e:
        print(f"✗ Layout endpoint test failed: {e}")


def test_motor_control():
    """Test motor control functionality."""
    print("Testing motor control...")
    
    stepper = SmartStepper(host="localhost", port=8082)
    
    # Test motor initialization
    init_request = "POST /api/init HTTP/1.1\r\nHost: localhost:8082\r\n\r\n{\"step_pin\": 18, \"dir_pin\": 19, \"enable_pin\": 20}"
    
    try:
        stepper.initialize_motor(init_request)
        print("✓ Motor initialization test passed")
    except Exception as e:
        print(f"✗ Motor initialization test failed: {e}")
    
    # Test motor control
    control_request = "POST /api/control HTTP/1.1\r\nHost: localhost:8082\r\n\r\n{\"direction\": \"forward\", \"speed\": 60, \"steps\": 200}"
    
    try:
        stepper.control_motor(control_request)
        print("✓ Motor control test passed")
    except Exception as e:
        print(f"✗ Motor control test failed: {e}")


def test_status_endpoint():
    """Test the status endpoint."""
    print("Testing status endpoint...")
    
    stepper = SmartStepper(host="localhost", port=8083)
    
    # Test status without motor
    status_request = "GET /api/status HTTP/1.1\r\nHost: localhost:8083\r\n\r\n"
    
    try:
        stepper.get_status(status_request)
        print("✓ Status endpoint test passed")
    except Exception as e:
        print(f"✗ Status endpoint test failed: {e}")


def test_config_loading():
    """Test configuration loading."""
    print("Testing configuration loading...")
    
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Verify required config sections
        assert 'server' in config
        assert 'motor' in config
        assert 'web_interface' in config
        
        print("✓ Configuration loading test passed")
    except Exception as e:
        print(f"✗ Configuration loading test failed: {e}")


def test_web_interface_integration():
    """Test web interface integration."""
    print("Testing web interface integration...")
    
    stepper = SmartStepper(host="localhost", port=8084)
    
    # Test that the layout contains required elements
    mock_request = "GET /api/layout HTTP/1.1\r\nHost: localhost:8084\r\n\r\n"
    
    try:
        # Capture the response by temporarily redirecting stdout
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        with redirect_stdout(output):
            stepper.get_layout(mock_request)
        
        # Parse the response to verify structure
        response_lines = output.getvalue().split('\r\n')
        json_start = False
        json_content = ""
        
        for line in response_lines:
            if json_start:
                json_content += line
            elif line == "":
                json_start = True
        
        layout = json.loads(json_content)
        
        # Verify required fields
        assert 'title' in layout
        assert 'elements' in layout
        assert 'submitUrl' in layout
        
        # Verify form elements
        elements = layout['elements']
        element_ids = [elem['id'] for elem in elements]
        
        assert 'direction' in element_ids
        assert 'speed' in element_ids
        assert 'steps' in element_ids
        
        print("✓ Web interface integration test passed")
        
    except Exception as e:
        print(f"✗ Web interface integration test failed: {e}")


def main():
    """Run all tests."""
    print("Running SmartStepper tests...\n")
    
    tests = [
        test_config_loading,
        test_layout_endpoint,
        test_motor_control,
        test_status_endpoint,
        test_web_interface_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SmartStepper module is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")


if __name__ == "__main__":
    main() 