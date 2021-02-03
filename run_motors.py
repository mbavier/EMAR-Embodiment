#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

#
# *********     Protocol Combined Example      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 1.0 and 2.0
# This example is tested with a Dynamixel MX-28, a Dynamixel PRO 54-200 and an USB2DYNAMIXEL
# Be sure that properties of Dynamixel MX and PRO are already set as %% MX - ID : 1 / Baudnum : 34 (Baudrate : 57600) , PRO - ID : 1 / Baudnum : 1 (Baudrate : 57600)
#

# Be aware that:
# This example configures two different control tables (especially, if it uses Dynamixel and Dynamixel PRO). It may modify critical Dynamixel parameter on the control table, if Dynamixels have wrong ID.
#

import os

def writeToAddr(addr, input_data, motor_id, size_in_bytes, portHandler, packetHandler):
    if (size_in_bytes == 1):
        result, error = packetHandler.write1ByteTxRx(portHandler, motor_id, addr, input_data)
    elif (size_in_bytes == 2):
        result, error = packetHandler.write2ByteTxRx(portHandler, motor_id, addr, input_data)
    else: #(size_in_bytes == 4)
        result, error = packetHandler.write4ByteTxRx(portHandler, motor_id, addr, input_data)
    return result, error

def readAddr(addr, motor_id, size_in_bytes, portHandler, packetHandler):
    if (size_in_bytes == 1):
        data, result, error = packetHandler.read1ByteTxRx(portHandler, motor_id, addr)
    elif (size_in_bytes == 2):
        data, result, error = packetHandler.read2ByteTxRx(portHandler, motor_id, addr)
    else: #(size_in_bytes == 4)
        data, result, error = packetHandler.read4ByteTxRx(portHandler, motor_id, addr)
    return data, result, error


if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address for Dynamixel MX
ADDR_MX_TORQUE_ENABLE       = 64               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION       = 116
ADDR_MX_PRESENT_POSITION    = 132

# Control table address for Dynamixel PRO
ADDR_PRO_TORQUE_ENABLE      = 64
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132
ADDR_PRO_GOAL_VELOCITY      = 104
ADDR_PRO_PROFILE_VELOCITY   = 112 # Between -(Velocity Limit) and (Velocity Limit)
ADDR_PRO_PROFILE_ACCEL      = 108

ADDR_VELOCITY_LIMIT         = 44 # Between 0 and 1023
ADDR_MOVING_THRESHOLD       = 24 # Present Velocity must be > Threshold for movement to occur

# Protocol version
PROTOCOL_VERSION2           = 2.0

# Default setting
DXL2_ID                     = 1                 # Dynamixel#2 ID : 
                                                # 1 - A, 2 - B
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM4'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL2_MINIMUM_POSITION_VALUE = 100 
DXL2_MAXIMUM_POSITION_VALUE = 4000
DXL2_MOVING_STATUS_THRESHOLD = 20                # Dynamixel PRO moving status threshold

index = 0
dxl2_goal_position = [DXL2_MINIMUM_POSITION_VALUE, DXL2_MAXIMUM_POSITION_VALUE]         # Goal position of Dynamixel PRO

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler2 = PacketHandler(PROTOCOL_VERSION2)


# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

comm_results, error = writeToAddr(ADDR_VELOCITY_LIMIT, 500, DXL2_ID, 4, portHandler, packetHandler2)
maxVelocity, comm_results, error = readAddr(ADDR_VELOCITY_LIMIT, DXL2_ID, 4, portHandler, packetHandler2)
print(maxVelocity)
movingThresh, comm_results, error = readAddr(ADDR_MOVING_THRESHOLD, DXL2_ID, 4, portHandler, packetHandler2)
print(movingThresh)

comm_results, error = writeToAddr(ADDR_PRO_GOAL_VELOCITY, 50, DXL2_ID, 4, portHandler, packetHandler2)

# Enable Dynamixel#2 Torque
dxl_comm_result, dxl_error = writeToAddr(ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE, DXL2_ID, 1, portHandler, packetHandler2)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler2.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL2_ID)

while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break
    # Write Dynamixel#2 goal position
    dxl_comm_result, dxl_error = writeToAddr(ADDR_PRO_GOAL_POSITION, dxl2_goal_position[index], DXL2_ID, 4, portHandler, packetHandler2)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler2.getRxPacketError(dxl_error))


    while 1:
        presnetVelocity, comm_results, error = readAddr(ADDR_PRO_GOAL_VELOCITY, DXL2_ID, 4, portHandler, packetHandler2)
        print(presnetVelocity)
        # Read Dynamixel#2 present position
        dxl2_present_position, dxl_comm_result, dxl_error = readAddr(ADDR_PRO_PRESENT_POSITION, DXL2_ID, 4, portHandler, packetHandler2)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler2.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL2_ID, dxl2_goal_position[index], dxl2_present_position))

        if not ((abs(dxl2_goal_position[index] - dxl2_present_position) > DXL2_MOVING_STATUS_THRESHOLD)):
            break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0    

# Disable Dynamixel#2 Torque
dxl_comm_result, dxl_error = writeToAddr(ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE, DXL2_ID, 1, portHandler, packetHandler2)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler2.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
