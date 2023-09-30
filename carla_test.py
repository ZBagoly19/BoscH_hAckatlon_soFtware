import math
import time
import csv
import carla
from carla import Transform, Location, Rotation

########################################################################################################################
# Put stuff on the map based on the [0] line of the dataset

# Connect to the client and get the world object
# for network computer, 'localhost' should be full IP address; port number
client = carla.Client('localhost', 2000)
world = client.get_world()
client.set_timeout(10.0) # seconds

# to create objects: vehicles, pedestrians, props
bp_lib = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

# Get the blueprint for the vehicle you want ('vehicle.lincoln.mkz_2020' works)
vehicle_bp = bp_lib.find('vehicle.ford.mustang')
# vehicle_bp.set_attribute('color', '255,0,0')

# Try spawning the vehicle at a randomly chosen spawn point
#random.choice(spawn_points)
print("Number of spawn points:", len(spawn_points))
vehicle = world.try_spawn_actor(vehicle_bp, spawn_points[0])
