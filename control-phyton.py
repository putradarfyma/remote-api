# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 14:35:32 2019

@author: darfyma
"""

import vrep
import time 
#import math 
import sys

import numpy as np
#import skfuzzy as fuzz
#from skfuzzy import control as ctrl
     
    



vrep.simxFinish(-1) 
clientID=vrep.simxStart ('127.0.0.1',19997,True,True,5000,5)

if clientID!=-1:
    print ("Connected to remote API server") 
    vrep.simxAddStatusbarMessage(clientID,"Program Loaded!",vrep.simx_opmode_oneshot)
else: 
    print ("Connection not successful")
    sys.exit("Could not connect")
    
time.sleep(1)

sensor_h=0 
sensor_val=0 


vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait)

errorCode,left_motor_handle=vrep.simxGetObjectHandle(clientID,"Pioneer_p3dx_leftMotor",vrep.simx_opmode_oneshot_wait) 
errorCode,right_motor_handle=vrep.simxGetObjectHandle(clientID,"Pioneer_p3dx_rightMotor",vrep.simx_opmode_oneshot_wait)
errorCode,sensor_h=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor1',vrep.simx_opmode_blocking) 
errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor_h,vrep.simx_opmode_streaming)
 
    
time.sleep(0.2)


while (1): 

#    for x in range (0,16):
    
    
    sensor_val = np.linalg.norm(detectedPoint)
    if sensor_val >= 1.0:
        sensor_val = 0   
        
    sensor_val_round = round(sensor_val,2)
            
    errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor_h,vrep.simx_opmode_buffer)
   
    
    
    
    
    
    print(sensor_val_round)    
    
    
    errorCode=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle,0, vrep.simx_opmode_streaming)
    errorCode=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0, vrep.simx_opmode_streaming)
 
    
    
