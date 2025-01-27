"""Markov_Localization controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

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

ground = robot.getDevice('gs0')
ground.enable(time_step)


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

def ensure_right_direction():
    if(is_front_obastacle()):
        move(-max_speed)
    elif(is_back_obastacle()):
        move(max_speed)    

WHITE, BLACK = 1, 0

last_seen_color = WHITE

def switched_tiles():
    if ground.getValue():
    

current_tile = 0

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(time_step) != -1:
    ensure_right_direction()
    
    if switched_tiles():
        
    
    print(ground.getValue())
        

        
    # print(left_ir.getValue(), right_ir.getValue(), "\n")
    pass








