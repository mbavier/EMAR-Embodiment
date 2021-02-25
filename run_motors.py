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
# Control table address for Dynamixel PRO
from dynamixel_sdk import *  

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



def motorInitialize(device_port="COM4", protocol_version=2.0, BAUDRATE=57600):
    portHandler = PortHandler(device_port)
    packetHandler = PacketHandler(protocol_version)
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
    # Torque Enable - Addr 64
    return portHandler, packetHandler

def turnOnMotors(motor_id, portHandler, packetHandler):
    result, error = writeToAddr(64, 1, motor_id, 1, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    else:
        print("Dynamixel#%d has been successfully connected" % motor_id)

def turnOffMotors(motor_id, portHandler, packetHandler):
    # Torque Enable - Addr 64
    result, error = writeToAddr(64, 0, motor_id, 1, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    # Close port
    portHandler.closePort()


def moveMotorTo(motor_id, pos, portHandler, packetHandler):
    result, error = writeToAddr(116, pos, motor_id, 4, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    # Wait  for motor to get to that position
    while 1:
        # Read Dynamixel#2 present position
        pres_pos = getPresPosition(motor_id, portHandler, packetHandler)

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (motor_id, pos, pres_pos))

        if not (abs(pos - pres_pos) > 20): # 20 is moving status threshold
            break

def moveTwoMotorsTo(motor_id, pos, portHandler, packetHandler, motor_id2, pos2, portHandler2, packetHandler2):
    result, error = writeToAddr(116, pos, motor_id, 4, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    result, error = writeToAddr(116, pos2, motor_id2, 4, portHandler2, packetHandler2)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    while 1:
        # Read Dynamixel#2 present position
        pres_pos = getPresPosition(motor_id, portHandler, packetHandler)
        pres_pos2 = getPresPosition(motor_id2, portHandler2, packetHandler2)
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (motor_id, pos, pres_pos))
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (motor_id2, pos2, pres_pos2))
        if not (abs(pos - pres_pos) > 20 & abs(pos2 - pres_pos2) >): # 20 is moving status threshold
            break
    
def getPresPosition(motor_id, portHandler, packetHandler):
    pres_pos, result, error = readAddr(132, motor_id, 4, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    return pres_pos

def setVelocity(motor_id, velocity, portHandler, packetHandler):
    result, error = writeToAddr(112, velocity, motor_id, 4, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))

def setAcceleration(motor_id, acceleration, portHandler, packetHandler):
    result, error = writeToAddr(108, acceleration, motor_id, 4, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))

def setGoalPWM(motor_id, pwm, portHandler, packetHandler):
    result, error = writeToAddr(100, pwm, motor_id, 2, portHandler, packetHandler)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))