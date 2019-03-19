
'''while we are connected:'''
    
    
import vrep
import time 
import sys
#import numpy as np


    
vrep.simxFinish(-1) 
clientID=vrep.simxStart ('127.0.0.1',19997,True,True,5000,5)

if clientID!=-1:

    print ("Connected to remote API server") 
    vrep.simxAddStatusbarMessage(clientID,"Program Loaded!",vrep.simx_opmode_oneshot)
else: 
    print ("Connection not successful")
    sys.exit("Could not connect")
    
time.sleep(1)

vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait)


#err,signal=vrep.simxReadStringStream(clientID,"toClient",vrep.simx_opmode_streaming)
err,signal=vrep.simxGetFloatSignal(clientID,"toClient",vrep.simx_opmode_streaming)

#simxInt simxGetFloatSignal(simxFloat* signalValue,simxInt operationMode)

while vrep.simxGetConnectionId(clientID) != -1:
  
  
    
  err,signal=vrep.simxGetFloatSignal(clientID,"toClient",vrep.simx_opmode_buffer)	
  if (err==vrep.simx_return_ok):  
    '''Data produced by the child script was retrieved! Send it back to the child script:'''
    #vrep.simxWriteStringStream(clientID,"fromClient",signal,vrep.simx_opmode_oneshot)
    print (signal) 
  




    
 

    