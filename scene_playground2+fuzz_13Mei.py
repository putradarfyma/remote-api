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

lf = np.arange(0,1, 0.001)

left  = ctrl.Antecedent(lf, 'left')
right = ctrl.Antecedent(lf, 'right')

out = ctrl.Consequent(np.arange(-3, 3, 0.001), 'output')

left['jauh']  = fuzz.gaussmf(left.universe,0.645,0.07)
left['sedang']= fuzz.gaussmf(left.universe,0.340,0.07)
left['dekat'] = fuzz.gaussmf(left.universe,0.100,0.07)

right['jauh'] = fuzz.gaussmf(right.universe,0.645,0.07)
right['sedang'] = fuzz.gaussmf(right.universe,0.340,0.07)
right['dekat'] = fuzz.gaussmf(right.universe,0.100,0.07)

#s8['jauh'] = fuzz.gaussmf(s8.universe,0.25,0.07)
#s8['sedang'] = fuzz.gaussmf(s8.universe,0.5,0.07)
#s8['dekat'] = fuzz.gaussmf(s8.universe,0.75,0.07)

#s9['jauh'] = fuzz.gaussmf(s9.universe,0.25,0.07)
#s9['sedang'] = fuzz.gaussmf(s9.universe,0.5,0.07)
#s9['dekat'] = fuzz.gaussmf(s9.universe,0.75,0.07)

out['lambat'] = fuzz.gaussmf(out.universe,0,0.5)
out['sedang'] = fuzz.gaussmf(out.universe,1.5,0.5)
out['cepat'] = fuzz.gaussmf(out.universe,3,0.5)


##out roda kiri (susur kiri)

rule1 = ctrl.Rule(left['jauh']   | right['dekat'],    out['cepat'])  
rule2 = ctrl.Rule(left['jauh']   | right['sedang'],   out['cepat'])
rule3 = ctrl.Rule(left['jauh']   | right['jauh'],    out['lambat'])   

rule4 = ctrl.Rule(left['sedang'] | right['dekat'],   out['sedang']) 
rule5 = ctrl.Rule(left['sedang'] | right['sedang'],   out['lambat']) #center 
rule6 = ctrl.Rule(left['sedang'] | right['jauh'],    out['sed_cep']) 

rule7 = ctrl.Rule(left['dekat']  | right['dekat'],  out['lambat'])  
rule8 = ctrl.Rule(left['dekat']  | right['sedang'],   out['lambat'])
rule9 = ctrl.Rule(left['dekat']  | right['jauh'],     out['sed_cep'])

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
            
            val_s[i]=round(signal,2)       
                
#------------------------------------------------------------------------------                
    #note sensor kiri, s1 = val_s[2],s16 = val_s[17]
    #note sensor kanan, s8 = val_s[9],s9 = val_s[10]
    sensleft = (val_s[2]+val_s[17])/2
    sensright= (val_s[8]+val_s[9])/2
    
    erorr = sensleft - sensright
    
    
    outing.input['left'] = sensleft
    outing.input['right'] = sensright
    
    outing.compute()
    
    c = outing.output['output']
    
    err=vrep.simxSetFloatSignal(clientID,'vLeft',2 ,vrep.simx_opmode_oneshot)
    err=vrep.simxSetFloatSignal(clientID,'vRight',2+c,vrep.simx_opmode_oneshot)
    
    print(round(sensleft,4),round(sensright,4),round(erorr,4), round(c,1) )
    
    
    
