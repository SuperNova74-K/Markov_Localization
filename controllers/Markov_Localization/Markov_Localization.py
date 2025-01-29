"""Markov_Localization controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Camera
import cupy as np


# create the Robot instance.
robot = Robot()

# get the time step of the current world.
time_step = int(robot.getBasicTimeStep())


max_speed = 6.28
left_motor = robot.getMotor('left wheel motor')
right_motor = robot.getMotor('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

irs=[]
for i in range(8):
    irs.append(robot.getDevice(f'ps{i}'))
    irs[-1].enable(time_step)

ground_camera = robot.getDevice('gcam')
ground_camera.enable(time_step)

left_ir = irs[5]
right_ir = irs[2]

def move(speed=max_speed):
    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)

def is_front_obastacle():
    return (irs[0].getValue() > 100) and (irs[7].getValue() > 100)

def is_back_obastacle():
    return (irs[4].getValue() > 100) and (irs[3].getValue() > 100)

move()

current_tile_index = 0
movement_direction = 1

def ensure_right_direction():
    global movement_direction

    if is_front_obastacle():
        move(-max_speed)
        movement_direction *= -1
    elif is_back_obastacle():
        move(max_speed)
        movement_direction *= -1


WHITE, BLACK = 1, 0

def get_ground_tile_color():
    # Get image from camera as a byte string
    image = ground_camera.getImage()

    # Convert to NumPy array and reshape to (height, width, 4) since Webots uses BGRA
    img_array = np.frombuffer(image, dtype=np.uint8).reshape((ground_camera.getHeight(), ground_camera.getWidth(), 4))

    # Extract RGB channels and compute grayscale
    grayscale_matrix = img_array[:, :, :3].mean(axis=2)  # Average RGB channels

    # Compute average grayscale value
    avg_grayscale = np.mean(grayscale_matrix)

    # Determine if tile is black or white
    return WHITE if avg_grayscale > 127 else BLACK  # Thresholding at 127


last_seen_color = WHITE

def switched_tiles():
    global last_seen_color

    ground_tile_color = get_ground_tile_color()

    if ground_tile_color != last_seen_color:
        last_seen_color = ground_tile_color
        return True
    return False


markov_beliefs = [1/7] * 7

wall = [1, 0, 0, 1, 0, 1, 0]
open_door = [0, 1, 0, 0, 1, 0, 0]
open_hallway = [0, 0, 1, 0, 0, 0, 1]

def sensed_status():
    left_ir.getValue()

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(time_step) != -1:
    ensure_right_direction()

    print(left_ir.getValue())    
    # if switched_tiles():
    #     current_tile_index += movement_direction
    #     print(f"We are On{current_tile_index}")
    #
    #     # Markov
    #     sensed_status()








