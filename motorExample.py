from run_motors import *
import time

portH, packetH = motorInitialize(1)
comm_results, error = writeToAddr(11, 3, 1, 1, portH, packetH)

# set maximum velocity to 1023
comm_results, error = writeToAddr(44, 1023, 1, 4, portH, packetH)

if (getPresPosition(1, portH, packetH) >= 3990):
    goal_pos = 0
else:
    goal_pos = 4000

# Set max velocity
setVelocity(1, 500, portH, packetH)

# Sets max acceleration, will never go above 50% of velocity
setAcceleration(1, 45, portH, packetH)

# Set goal PWM
setGoalPWM(1, 100, portH, packetH)

start = time.time()
moveMotorTo(1, goal_pos, portH, packetH)
end = time.time()
print(end - start)

turnOffMotors(1, portH, packetH)