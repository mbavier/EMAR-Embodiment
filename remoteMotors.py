import requests
import time
import json
from run_motors import *

# Initialization

# Dummy data for motors
# Currently stored as an array corresponding to [motor 1, motor 2]
motor_values = {"head_0": -1, "head_1": -1, "body_0": -1, "body_1": -1}
motor_id_list = [4, 5, 2, 3]
new_motor_values = {"head_0": -1, "head_1": -1, "body_0": -1, "body_1": -1}

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

portH, packetH = motorInitialize("/dev/tty.usbserial-FT4TFNM7")
#turnOnMotors(1, portH, packetH)
turnOnMotors(2, portH, packetH)
turnOnMotors(3, portH, packetH)
turnOnMotors(4, portH, packetH)
turnOnMotors(5, portH, packetH)


comm_results, error = writeToAddr(11, 3, 2, 1, portH, packetH)
comm_results, error = writeToAddr(11, 3, 3, 1, portH, packetH)
comm_results, error = writeToAddr(11, 3, 4, 1, portH, packetH)
comm_results, error = writeToAddr(11, 3, 5, 1, portH, packetH)

#moveMotorTo(1, goal_pos0, portH, packetH)
#moveMotorTo(2, goal_pos1, portH, packetH)
moveMotorListTo([2, 3, 4, 5], [0, 4000, 0, 4000], portH, packetH)
# Main loop


while(True):

	# Sending get request and obtaining the response
	get_request = connection.get(url = URL + "robots.json")
	# Extracting data in json format 
	robots = get_request.json()
	
	##############
	# Check if there is a new motor value in the database
	##############
	web_data = robots[this_robot_id]["state"]["motors"]
	values_updated = False
	for motor_data in web_data:
		
		if(motor_values[motor_data['name']] != motor_data['value']):
			values_updated = True
			new_motor_values[motor_data['name']] = motor_data['value']
	if (values_updated):
		print("New motor values: " + str(new_motor_values))
		# TODO: Do something with the new motor values
		motor_values = new_motor_values
		motor_value_list = list(motor_values.values())
		moveMotorListTo(motor_id_list, motor_value_list, portH, packetH)
	time.sleep(0.1)