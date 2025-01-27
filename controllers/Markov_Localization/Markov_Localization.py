"""Markov_Localization controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
time_step = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

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

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(time_step) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    
    front, back = is_front_obastacle(), is_back_obastacle()
    
    if(front):
        move(-max_speed)
    elif(back):
        move(max_speed)

        
    print(left_ir.getValue(), right_ir.getValue(), "\n")
    pass

# Enter here exit cleanup code.
