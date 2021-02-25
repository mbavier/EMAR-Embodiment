import requests
import time
import json
from run_motors import *

# Initialization

# Dummy data for motors
# Currently stored as an array corresponding to [motor 1, motor 2]
motor_values = [-1, -1]

# Robot from database to listen to
this_robot_id = 0
# Firebase database parameters
api_key = ""
URL = "https://emar-database.firebaseio.com/"
AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + api_key;
headers = {'Content-type': 'application/json'}
auth_req_params = {"returnSecureToken":"true"}

# Start connection to Firebase and get anonymous authentication
connection = requests.Session()
connection.headers.update(headers)
auth_request = connection.post(url=AUTH_URL, params=auth_req_params)
auth_info = auth_request.json()
auth_params = {'auth': auth_info["idToken"]}

portH, packetH = motorInitialize("COM3")
turnOnMotors(1, portH, packetH)
comm_results, error = writeToAddr(11, 3, 1, 1, portH, packetH)
comm_results, error = writeToAddr(11, 3, 1, 1, portH, packetH)

if (getPresPosition(1, portH, packetH) >= 3990):
    goal_pos0 = 0
else:
    goal_pos0 = 4000

if (getPresPosition(1, portH, packetH) >= 3990):
    goal_pos1 = 0
else:
    goal_pos1 = 4000

#moveMotorTo(1, goal_pos0, portH, packetH)
#moveMotorTo(2, goal_pos1, portH, packetH)
moveTwoMotorsTo(1, goal_pos0, portH, packetH, 2, goal_pos1, portH, packetH)
# Setup motors
setVelocity(1, 500, portH, packetH)
setVelocity(2, 500, portH, packetH)

# Sets max acceleration, will never go above 50% of velocity
setAcceleration(1, 45, portH, packetH)
setAcceleration(2, 45, portH, packetH)

# Set goal PWM
setGoalPWM(1, 100, portH, packetH)
setGoalPWM(2, 100, portH, packetH)

# Main loop


while(True):

	# Sending get request and obtaining the response
	get_request = connection.get(url = URL + "robots.json")
	# Extracting data in json format 
	robots = get_request.json()
	
	##############
	# Check if there is a new motor value in the database
	##############
	robot_state = robots[this_robot_id]["state"]
	new_motor_values = [robot_state["motor0"], robot_state["motor1"]]
	if (motor_values != new_motor_values):
		print("New motor values: " + str(new_motor_values))
		# TODO: Do something with the new motor values
		motor_values = new_motor_values
		moveTwoMotorsTo(1, motor_values[0], portH, packetH, 2, motor_values[1], portH, packetH)
	time.sleep(0.1)