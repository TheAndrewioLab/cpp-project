from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

# Connect to the Vehicle
connection_string = '127.0.0.1:14550'
print('Connecting to vehicle on:', connection_string)
vehicle = connect(connection_string, wait_ready=True)

print("Connected to vehicle")

def get_location_metres(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the specified `original_location`. 
    The returned Location has the same `alt` value as `original_location`.
    """
    earth_radius = 6378137.0 # Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180.0))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180.0/math.pi)
    newlon = original_location.lon + (dLon * 180.0/math.pi)
    return LocationGlobalRelative(newlat, newlon, original_location.alt)

def move_right(vehicle, distance):
    """
    Move the vehicle to the right by a specified distance.
    """
    current_location = vehicle.location.global_relative_frame
    # Calculate the new location to the right
    new_location = get_location_metres(current_location, 0, distance)
    vehicle.simple_goto(new_location)

    while True:
        current_position = vehicle.location.global_relative_frame
        distance_to_target = get_distance_metres(current_position, new_location)
        print(f"Distance to target: {distance_to_target} meters")
        if distance_to_target < 1:
            print("Reached target location")
            break
        time.sleep(1)

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    This method is an approximation, and will not be accurate over large distances and close to the earth's poles.
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

# Example usage: Move the drone 5 meters to the right
move_right(vehicle, 5)

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
