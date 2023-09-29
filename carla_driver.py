# pip install carla --user
# install package after import fails

# python 3.7 needed

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
print("Number of spawn poins:", len(spawn_points))
vehicle = world.try_spawn_actor(vehicle_bp, spawn_points[0])

with open('data/DevelopmentData.csv') as csvfile:
    data_reader = list(csv.reader(csvfile, delimiter=','))
obj1_x = data_reader[0][0]
obj1_y = data_reader[0][1]
obj2_x = data_reader[0][2]
obj2_y = data_reader[0][3]
obj3_x = data_reader[0][4]
obj3_y = data_reader[0][5]
obj4_x = data_reader[0][6]
obj4_y = data_reader[0][7]

# Add pedestrians
pedestrian_bp = bp_lib.find('walker.pedestrian.0049')
transform_p1 = Transform(vehicle.get_transform().transform(Location(x=obj1_x, z=obj1_y)), Rotation(yaw=180))
pedestrian_1 = world.try_spawn_actor(pedestrian_bp, transform_p1)
pedestrian_bp = bp_lib.find('walker.pedestrian.0048')
transform_p2 = Transform(vehicle.get_transform().transform(Location(x=obj2_x, z=obj2_y)))
pedestrian_2 = world.spawn_actor(pedestrian_bp, transform_p2)
pedestrian_bp = bp_lib.find('walker.pedestrian.0047')
transform_p3 = Transform(vehicle.get_transform().transform(Location(x=obj3_x, z=obj3_y)))
pedestrian_3 = world.spawn_actor(pedestrian_bp, transform_p3)
pedestrian_bp = bp_lib.find('walker.pedestrian.0046')
transform_p4 = Transform(vehicle.get_transform().transform(Location(x=obj4_x, z=obj4_y)))
pedestrian_4 = world.spawn_actor(pedestrian_bp, transform_p4)

# Spawn an RGB camera with an offset from the vehicle center
# We could do it with multiple: bird eye, side-view etc.
camera_bp = bp_lib.find('sensor.camera.rgb')
camera_init_trans_above = Transform(Location(z=2))
camera_above = world.spawn_actor(camera_bp, camera_init_trans_above, attach_to=vehicle)
camera_init_trans_bird_eye = carla.Transform(Location(z=20), carla.Rotation(pitch=-75))
camera_bird_eye = world.spawn_actor(camera_bp, camera_init_trans_bird_eye, attach_to=vehicle)
camera_init_trans_behind = carla.Transform(Location(x=-6, z=2))
camera_behind = world.spawn_actor(camera_bp, camera_init_trans_behind, attach_to=vehicle)

########################################################################################################################
# Moving stuff based on the [1 : -1] lines of the data

for row in data_reader:

    # Move the spectator behind the vehicle
    spectator = world.get_spectator()
    transform = Transform(vehicle.get_transform().transform(Location(x=-4, z=2.5)), vehicle.get_transform().rotation)
    spectator.set_transform(transform)

    # Move vehicle
    location = vehicle.get_location()
    location.x = row[37]
    location.y = row[38]
    vehicle.set_location(location)
    print("Vehicle velocity:", vehicle.get_velocity())

    # Move objects
    location = vehicle.get_location()
    location.x += 2.0
    location.y += 2.0
    pedestrian_1.set_location(location)

    location = vehicle.get_location()
    location.x += 1.0
    location.y += 1.0
    pedestrian_2.set_location(location)

    # Add traffic to the simulation
    # for i in range(30):
    #     vehicle_bp = random.choice(bp_lib.filter('vehicle'))
    #     npc = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))

    # Set the all vehicles in motion using the Traffic Manager
    # for v in world.get_actors().filter('*vehicle*'):
    #     v.set_autopilot(True)

    control = carla.WalkerBoneControlIn()
    first_tuple = ('crl_hand__R', carla.Transform(rotation=carla.Rotation(roll=180)))
    control.bone_transforms = [first_tuple]
    pedestrian_1.apply_control(control)

    camera_above.listen(lambda image: image.save_to_disk('out/%06d_above.png' % image.frame))
    camera_above.stop()

    camera_bird_eye.listen(lambda image: image.save_to_disk('out/%06d_bird_eye.png' % image.frame))
    camera_bird_eye.stop()

    camera_behind.listen(lambda image: image.save_to_disk('out/%06d_behind.png' % image.frame))
    camera_behind.stop()
