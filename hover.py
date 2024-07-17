import time
import serial
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import argparse

# Function to set up the vehicle to hover
def hover(vehicle):
    print("Setting vehicle to hover at current location")
    vehicle.mode = VehicleMode("GUIDED")
    location = vehicle.location.global_relative_frame
    vehicle.simple_goto(location)

# Function to send data via UART
def send_uart_data(serial_port, data):
    serial_port.write(data.encode())

# Connect to the vehicle
connection_string = '127.0.0.1:14550'
print('Connecting to vehicle on:', connection_string)
vehicle = connect(connection_string, wait_ready=True)

# Set up UART connection
#uart_port = '/dev/tty0'  # Replace with your actual serial port
# baud_rate = 9600  # Adjust to your baud rate

#try:
    #serial_port = serial.Serial(uart_port, baud_rate, timeout=1)
#except serial.SerialException as e:
    #print(f"Error opening serial port {uart_port}: {e}")
   # exit(1)

def arm_and_takeoff(target_altitude):
    """
    Arms vehicle and fly to target_altitude.
    """
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Arm and take off to 10 meters altitude
arm_and_takeoff(10)

# Hover at the current position
hover(vehicle)

# Example data to send via UART
data_to_send = "Hovering at 10 meters altitude"

# Send data via UART
#send_uart_data(serial_port, data_to_send)

# Keep the vehicle hovering and sending data
try:
    while True:
        # Maintain hover by sending the same location command periodically
        hover(vehicle)
        
        # Send data periodically
     #   send_uart_data(serial_port, data_to_send)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

# Close connections
print("Close vehicle object and UART connection")
vehicle.close()
#serial_port.close()

 

