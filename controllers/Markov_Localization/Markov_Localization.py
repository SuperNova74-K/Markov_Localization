"""Markov_Localization controller."""
from controller import Robot, Camera
import cupy as cp

robot = Robot()

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
    img_array = cp.frombuffer(image, dtype=cp.uint8).reshape((ground_camera.getHeight(), ground_camera.getWidth(), 4))

    # Extract RGB channels and compute grayscale
    grayscale_matrix = img_array[:, :, :3].mean(axis=2)  # Average RGB channels

    # Compute average grayscale value
    avg_grayscale = cp.mean(grayscale_matrix)

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

import numpy as cp
import seaborn as sns
import matplotlib.pyplot as plt
plot_number = 0

def plot_beliefs(vector):
    global plot_number
    # Reshape to a 2D array (single-row heatmap)
    heatmap_data = vector.reshape(1, -1)

    # Plot the heatmap with fixed color scale (0 to 1)
    fig, ax = plt.subplots(figsize=(8, 1.5))
    sns.heatmap(heatmap_data, cmap='flare', cbar=True, xticklabels=False, yticklabels=False, ax=ax, vmin=0, vmax=1, fmt=".2f", annot_kws={"size": 10})

    # Remove axis labels
    plt.axis('off')

    save_path = f"C:/Users/kingk/Documents/webots/Markov_Localization/Results/{plot_number}"
    # Save the heatmap
    plt.savefig(save_path, dpi=250, bbox_inches='tight', pad_inches=0.5)
    plt.close()
    plot_number += 1

markov_beliefs = [1/7] * 7
markov_beliefs = cp.asarray(markov_beliefs)

plot_beliefs(markov_beliefs)

definition_matrix = [
    [1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1]
]
definition_matrix = cp.array(definition_matrix)

# wall = [1, 0, 0, 1, 0, 1, 0]
# open_door = [0, 1, 0, 0, 1, 0, 0]
# open_hallway = [0, 0, 1, 0, 0, 0, 1]

sensor_probability_matrix = [
    [0.7, 0.05, 0.001],
    [0.1 ,0.9, 0.1],
    [0, 0.001, 0.90]
]
sensor_probability_matrix = cp.array(sensor_probability_matrix)

class sensing_states:
    def __init__(self):
        self.wall = 0
        self.open_door = 1
        self.open_hallway = 2

sensing_states = sensing_states()

def sensed_status():
    value = left_ir.getValue()
    if value > 200:
        return sensing_states.wall
    elif value > 100:
        return sensing_states.open_door
    else:
        return sensing_states.open_hallway


while robot.step(time_step) != -1:
    ensure_right_direction()

    if switched_tiles():
        current_tile_index += movement_direction
        print(f"We are On{current_tile_index}")

        # Markov
        status = sensed_status()
        sense_vector = sensor_probability_matrix[status] @ definition_matrix
        update_vector = markov_beliefs * sense_vector
        normalized_result = update_vector / cp.sum(update_vector)

        # updating our beliefs
        markov_beliefs = normalized_result
        markov_beliefs = cp.roll(markov_beliefs, 1)
        markov_beliefs[0] = 0

        plot_beliefs(markov_beliefs)
