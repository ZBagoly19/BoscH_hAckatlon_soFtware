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
vehicle_bp.set_attribute('color', '255, 0, 0')

print(len(spawn_points))

# Try spawning the vehicle at a randomly chosen spawn point
#random.choice(spawn_points)
#transform = Transform(Location(x=230, y=195, z=40), Rotation(yaw=180))
vehicle = world.try_spawn_actor(vehicle_bp, spawn_points[0])



if vehicle is None:
    vehicle = world.get_actors().find(124)

print(world.get_actors())
# Add pedestrians
transform_p1 = Transform(vehicle.get_transform().transform(Location(x=11, y=-64)), Rotation(yaw=180))
loc = vehicle.get_location()
loc.y += +78
loc.z += 2
loc.x += +11
transfor2 = Transform(loc)
pedestrian_bp = bp_lib.find('walker.pedestrian.0019')
print(transfor2)
pedestrian_1 = world.try_spawn_actor(pedestrian_bp, transfor2)

# Move the spectator behind the vehicle
spectator = world.get_spectator()
transform = Transform(pedestrian_1.get_transform().transform(Location(x=-4, z=2.5)), pedestrian_1.get_transform().rotation)
spectator.set_transform(transform)
