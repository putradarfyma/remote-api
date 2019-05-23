# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:02:59 2019

@author: darfyma
"""
import vrep
import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl



#-------------------------Fuzzy Setup------------------------------------------


isar = np.arange(0,1, 0.01)
osar = np.arange(0,3, 0.01)

s1  = ctrl.Antecedent(isar, 'left_front')
s16 = ctrl.Antecedent(isar, 'left_back')

outLeft = ctrl.Consequent(osar, 'outputL')
outRight = ctrl.Consequent(osar, 'outputR')

#s1.automf(3)
#s16.automf(3)
outLeft.automf(5)
outRight.automf(5)

s1['poor']  = fuzz.trapmf (s1.universe,   [0   , 0    , 0.2 , 0.3  ])
s1['average']= fuzz.trapmf(s1.universe,   [0.2 , 0.3  , 0.37, 0.54 ])
s1['good'] = fuzz.trapmf  (s1.universe,   [0.37, 0.54 , 1   , 1    ])

s16['poor'] = fuzz.trapmf(s16.universe,   [0   , 0    , 0.2 , 0.3  ])
s16['average'] = fuzz.trapmf(s16.universe,[0.2 , 0.3  , 0.37, 0.54 ])
s16['good'] = fuzz.trapmf(s16.universe,   [0.37, 0.54 , 1   , 1    ])

#s8['jauh'] = fuzz.gaussmf(s8.universe,0.25,0.07)
#s8['sedang'] = fuzz.gaussmf(s8.universe,0.5,0.07)
#s8['dekat'] = fuzz.gaussmf(s8.universe,0.75,0.07)

#s9['jauh'] = fuzz.gaussmf(s9.universe,0.25,0.07)
#s9['sedang'] = fuzz.gaussmf(s9.universe,0.5,0.07)
#s9['dekat'] = fuzz.gaussmf(s9.universe,0.75,0.07)

#outRight['poor'] = fuzz.trapmf(outRight.universe,    [0  , 0.5, 2, 3 ])
#outRight['mediocre'] = fuzz.trapmf(outRight.universe,[0.5, 0.5, 3, 4 ])
#outRight['average'] = fuzz.trapmf(outRight.universe, [0  , 0.5, 4, 5 ])
#outRight['decent'] = fuzz.trapmf(outRight.universe,  [0  , 0.5, 5, 6 ])
#outRight['good'] = fuzz.trapmf(outRight.universe,    [0.5, 0.5, 6, 6 ])

#outLeft['poor'] = fuzz.trapmf(outLeft.universe,      [0  , 0.5, 2, 3])
#outLeft['mediocre'] = fuzz.trapmf(outLeft.universe,  [0.5, 0.5, 3, 4])
#outLeft['average'] = fuzz.trapmf(outLeft.universe,   [0  , 0.5, 4, 5])
#outLeft['decent'] = fuzz.trapmf(outLeft.universe,    [0  , 0.5, 5, 6])
#outLeft['good'] = fuzz.trapmf(outLeft.universe,      [0.5, 0.5, 6, 6])

#out roda kiri (susur kiri)
#poor,average,good
#poor,mediocre,average,decent,good 

rule1 = ctrl.Rule(s1['poor'   ]    & s16['poor'],    (outLeft['mediocre']  , outRight['poor']))  
rule2 = ctrl.Rule(s1['average']    & s16['poor'],    (outLeft['mediocre']  , outRight['poor']))
rule3 = ctrl.Rule(s1['good'   ]    & s16['poor'],    (outLeft['poor']      , outRight['mediocre']))   

rule4 = ctrl.Rule(s1['poor'   ]    & s16['average'], (outLeft['decent' ]   , outRight['average'])) 
rule5 = ctrl.Rule(s1['average']    & s16['average'], (outLeft['average']   , outRight['average'])) #center 
rule6 = ctrl.Rule(s1['good'   ]    & s16['average'], (outLeft['average']   , outRight['decent'])) 

rule7 = ctrl.Rule(s1['poor'   ]    & s16['good'],    (outLeft['mediocre']  , outRight['poor']))  
rule8 = ctrl.Rule(s1['average']    & s16['good'],    (outLeft['average']   , outRight['average']))
rule9 = ctrl.Rule(s1['good'   ]    & s16['good'],    (outLeft['average']   , outRight['good']))

 
outing_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9])
outing = ctrl.ControlSystemSimulation(outing_ctrl)
           
#-----------------------------Remote Api---------------------------------------

vrep.simxFinish(-1) 
clientID=vrep.simxStart ('127.0.0.1',19997,True,True,5000,5)
if clientID!=-1:
    print ("Connected to remote API server") 
    vrep.simxAddStatusbarMessage(clientID,"Program Loaded!",vrep.simx_opmode_oneshot)
else: 
    print ("Connection not successful")
    sys.exit("Could not connect")
    
vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait)
val_s=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
for x in range(0,18):
        err,signal=vrep.simxGetFloatSignal(clientID,'s'+str(x+1),vrep.simx_opmode_streaming)

#-----------------------------Looping------------------------------------------

while vrep.simxGetConnectionId(clientID) != -1:
          
    for i in range(0,18):      
        err,signal=vrep.simxGetFloatSignal(clientID,'s'+str(i+1),vrep.simx_opmode_buffer)	
        if (err==vrep.simx_return_ok):                         
            
            val_s[i]=signal       
                
#------------------------------------------------------------------------------                
    
    
    
    
    outing.input['left_front'] = val_s[2]
    outing.input['left_back']  = val_s[17]
    
    outing.compute()
    
    vl = outing.output['outputL']
    vr = outing.output['outputR']
    
    err=vrep.simxSetFloatSignal(clientID,'vLeft',(0) ,vrep.simx_opmode_oneshot)
    err=vrep.simxSetFloatSignal(clientID,'vRight',(0),vrep.simx_opmode_oneshot)
    
    aa = round(val_s[2],2)
    ab = round(val_s[17],2) 
    ac = round(vl,2)
    ad = round(vr,2)
    
#    ae = (str(aa)+" "+str(ab)+" || "+str(ac)+" "+str(ad))
    print(aa,ab," || ",ac,ad)
    
    




    
#    with open("test_data logger.csv","a") as f: 
#        write = csv.writer(f,delimiter=",")
#        write.writerow([time.time(),ae])
        
    

    
        
    
    
    
    