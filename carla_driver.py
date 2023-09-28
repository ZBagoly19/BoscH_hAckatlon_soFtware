# pip install carla --user
# install package after import fails

# python 3.7 needed

import math
import time
import random
import carla

# Connect to the client and get the world object
# for network computer, 'localhost' should be full IP address; port number
client = carla.Client('localhost', 2000)
world = client.get_world()

# to create objects: vehicles, pedestrians, props
bp_lib = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

# Get the blueprint for the vehicle you want
vehicle_bp = bp_lib.find('vehicle.lincoln.mkz_2020')

# Try spawning the vehicle at a randomly chosen spawn point
vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))

# Move the spectator behind the vehicle
spectator = world.get_spectator()
transform = carla.Transform(vehicle.get_transform().transform(carla.Location(x=-4, z=2.5)), vehicle.get_transform().rotation)
spectator.set_transform(transform)

# Add traffic to the simulation
for i in range(30):
    vehicle_bp = random.choice(bp_lib.filter('vehicle'))
    npc = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))

# Set the all vehicles in motion using the Traffic Manager
for v in world.get_actors().filter('*vehicle*'):
    v.set_autopilot(True)

# Spawn an RGB camera with an offset from the vehicle center
# We could do it with multiple: bird eye, side-view etc.
camera_bp = bp_lib.find('sensor.camera.rgb')
# questionable line: does it follow the vehicle's orientation?
camera_init_trans_above = carla.Transform(carla.Location(z=2))
camera_above = world.spawn_actor(camera_bp, camera_init_trans_above, attach_to=vehicle)
camera_init_trans_bird_eye = carla.Transform(carla.Location(z=20), carla.Rotation(pitch=-75))
camera_bird_eye = world.spawn_actor(camera_bp, camera_init_trans_bird_eye, attach_to=vehicle)
camera_init_trans_behind = carla.Transform(carla.Location(x=-6, z=2))
camera_behind = world.spawn_actor(camera_bp, camera_init_trans_behind, attach_to=vehicle)

# Start the camera saving data to 'out' directory
camera_above.listen(lambda image: image.save_to_disk('out/%06d_above.png' % image.frame))
camera_bird_eye.listen(lambda image: image.save_to_disk('out/%06d_bird_eye.png' % image.frame))
camera_behind.listen(lambda image: image.save_to_disk('out/%06d_behind.png' % image.frame))

# Stop the camera when we've recorded enough data (so in this form it only records 1 image)
camera_above.stop()
camera_bird_eye.stop()
camera_behind.stop()
