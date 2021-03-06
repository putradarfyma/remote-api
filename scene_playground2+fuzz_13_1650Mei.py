# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:02:59 2019
@author: HambaAllah
Dibuat dalam rangka Penugasan Penelitian Beasiswa Voucher Semester Ganjil 2018/2019 
"""

import time
import vrep
import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~List of Procedures~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
        
def forward(l,r):    
    vrep.simxSetFloatSignal(clientID,'vLeft',l ,vrep.simx_opmode_oneshot)
    vrep.simxSetFloatSignal(clientID,'vRight',r,vrep.simx_opmode_oneshot)

def backward (l,r):
    vrep.simxSetFloatSignal(clientID,'vLeft',-l ,vrep.simx_opmode_oneshot)
    vrep.simxSetFloatSignal(clientID,'vRight',-r,vrep.simx_opmode_oneshot)
    
def nothing (t):
    vrep.simxSetFloatSignal(clientID,'vLeft' ,0,vrep.simx_opmode_oneshot)
    vrep.simxSetFloatSignal(clientID,'vRight',0,vrep.simx_opmode_oneshot)
    time.sleep(t) 
def turnright(l,r):
    vrep.simxSetFloatSignal(clientID,'vLeft',l ,vrep.simx_opmode_oneshot)
    vrep.simxSetFloatSignal(clientID,'vRight',-r,vrep.simx_opmode_oneshot)
    
def sens_read():
    for i in range(0,18):      
        err,signal=vrep.simxGetFloatSignal(clientID,'s'+str(i+1),vrep.simx_opmode_buffer)	
        if (err==vrep.simx_return_ok):                         
            val_s[i]=signal

def fuzzy_config():
            
    #MF Parameter Input Trapezoidal_sensorkiri 
    trap_dekat_kiri_a= 0.0
    trap_dekat_kiri_b= 0.14
    
    trap_sedang_kiri_a=0.19
    trap_sedang_kiri_b=0.38
    
    trap_jauh_kiri_a=0.4
    trap_jauh_kiri_b=0.7
    
    
    #MF Parameter Output Triangular
    mid_stop = -1.5                                   #Range Input for Universe 
    mid_pelan = 0.5 
    mid_cepat = 1
    mid_c_cepat = 1.5
    mid_max_cepat =3                                  #Range Input for Universe
    
    #Universe Input and Output 
    isar = np.arange(trap_dekat_kiri_a,trap_jauh_kiri_b, 0.001)
    osar = np.arange(mid_stop,mid_max_cepat, 0.01)
    
    s1_left  = ctrl.Antecedent(isar, 'sensor_left')
    s2_front = ctrl.Antecedent(isar, 'sensor_leftfront')
#    s7_frontr= ctrl.Antecedent(isar, 'sensor_frontright')
#    s8_right = ctrl.Antecedent(isar, 'sensor_right')
    
    
    outLeft = ctrl.Consequent(osar, 'outputL')
    outRight = ctrl.Consequent(osar, 'outputR')
    
    
    s1_left['dekat']  = fuzz.trapmf (s1_left.universe,  [trap_dekat_kiri_a , trap_dekat_kiri_a  , trap_dekat_kiri_b , trap_sedang_kiri_a  ]) #0.01 , 0.15  , 0.20 , 0.3
    s1_left['sedang']= fuzz.trapmf(s1_left.universe,    [trap_dekat_kiri_b , trap_sedang_kiri_a , trap_sedang_kiri_b, trap_jauh_kiri_a ])
    s1_left['jauh'] = fuzz.trapmf  (s1_left.universe,   [trap_sedang_kiri_b, trap_jauh_kiri_a , trap_jauh_kiri_b  , trap_jauh_kiri_b  ])
    
    s2_front['dekat']  = fuzz.trapmf (s1_left.universe,  [trap_dekat_kiri_a , trap_dekat_kiri_a  , trap_dekat_kiri_b , trap_sedang_kiri_a  ]) #0.01 , 0.15  , 0.20 , 0.3
    s2_front['sedang']= fuzz.trapmf(s1_left.universe,    [trap_dekat_kiri_b , trap_sedang_kiri_a , trap_sedang_kiri_b, trap_jauh_kiri_a ])
    s2_front['jauh'] = fuzz.trapmf  (s1_left.universe,   [trap_sedang_kiri_b, trap_jauh_kiri_a , trap_jauh_kiri_b  , trap_jauh_kiri_b  ])

#    s7_frontr['dekat']  = fuzz.trapmf (s7_frontr.universe,  [trap_dekat_depan_a , trap_dekat_depan_a  , trap_dekat_depan_b , trap_sedang_depan_a  ])
#    s7_frontr['sedang']= fuzz.trapmf(s7_frontr.universe,    [trap_dekat_depan_b , trap_sedang_depan_a  , trap_sedang_depan_b , trap_jauh_depan_a ])
#    s7_frontr['jauh'] = fuzz.trapmf  (s7_frontr.universe,   [trap_sedang_depan_b, trap_jauh_depan_a , trap_jauh_depan_b  , trap_jauh_depan_b  ])
#    
#    s8_right['dekat']  = fuzz.trapmf (s8_right.universe,  [trap_dekat_kiri_a , trap_dekat_kiri_a  , trap_dekat_kiri_b , trap_sedang_kiri_a  ]) 
#    s8_right['sedang']= fuzz.trapmf(s8_right.universe,    [trap_dekat_kiri_b , trap_sedang_kiri_a , trap_sedang_kiri_b, trap_jauh_kiri_a ])
#    s8_right['jauh'] = fuzz.trapmf  (s8_right.universe,   [trap_sedang_kiri_b, trap_jauh_kiri_a , trap_jauh_kiri_b  , trap_jauh_kiri_b  ])
    

    outLeft['stop'] = fuzz.trimf(outRight.universe,       [mid_stop   ,  mid_stop, mid_pelan ])
    outLeft['pelan'] = fuzz.trimf(outRight.universe,      [mid_stop, mid_pelan, mid_cepat ])
    outLeft['cepat'] = fuzz.trimf(outRight.universe,      [mid_pelan, mid_cepat, mid_c_cepat ])
    outLeft['c_cepat'] = fuzz.trimf(outRight.universe,    [mid_cepat, mid_c_cepat, mid_max_cepat ])
    outLeft['max_cepat'] = fuzz.trimf(outRight.universe,  [mid_c_cepat, mid_max_cepat , mid_max_cepat    ])
    
    outRight['stop'] = fuzz.trimf(outRight.universe,       [mid_stop   ,  mid_stop, mid_pelan ])
    outRight['pelan'] = fuzz.trimf(outRight.universe,      [mid_stop, mid_pelan, mid_cepat ])
    outRight['cepat'] = fuzz.trimf(outRight.universe,      [mid_pelan, mid_cepat, mid_c_cepat ])
    outRight['c_cepat'] = fuzz.trimf(outRight.universe,    [mid_cepat, mid_c_cepat, mid_max_cepat ])
    outRight['max_cepat'] = fuzz.trimf(outRight.universe,  [mid_c_cepat, mid_max_cepat , mid_max_cepat    ])
    
    
    
    rule1 = ctrl.Rule(s1_left['dekat' ]  & s2_front['dekat']  , (outLeft['c_cepat']  , outRight['stop']))  
    rule2 = ctrl.Rule(s1_left['sedang']  & s2_front['dekat']  , (outLeft['max_cepat'], outRight['cepat']))
    rule3 = ctrl.Rule(s1_left['jauh'  ]  & s2_front['dekat']  , (outLeft['cepat']    , outRight['max_cepat']))   
    
    rule4 = ctrl.Rule(s1_left['dekat' ]  & s2_front['sedang'] , (outLeft['max_cepat'], outRight['stop'])) 
    rule5 = ctrl.Rule(s1_left['sedang']  & s2_front['sedang'] , (outLeft['max_cepat'], outRight['max_cepat'])) #center 
    rule6 = ctrl.Rule(s1_left['jauh'  ]  & s2_front['sedang'] , (outLeft['cepat']    , outRight['pelan'])) 
    
    rule7 = ctrl.Rule(s1_left['dekat' ]  & s2_front['jauh']   , (outLeft['stop']     , outRight['max_cepat']))  
    rule8 = ctrl.Rule(s1_left['sedang']  & s2_front['jauh']   , (outLeft['stop']     , outRight['max_cepat']))
    rule9 = ctrl.Rule(s1_left['jauh'  ]  & s2_front['jauh']   , (outLeft['stop']%0.5 , outRight['max_cepat']))
    
#    rule10 = ctrl.Rule(s1_left['dekat' ]  & s2_front['sedang'] & (s7_frontr['dekat'] | s8_right['dekat'])  , (outLeft['max_cepat']  , outRight['stop']))
#    rule11 = ctrl.Rule(s1_left['sedang']  & s2_front['sedang'] & (s7_frontr['dekat'] | s8_right['dekat']) , (outLeft['max_cepat']  , outRight['stop']))
#    rule12 = ctrl.Rule(s1_left['jauh'  ]  & s2_front['sedang'] & (s7_frontr['dekat'] | s8_right['dekat'])  , (outLeft['max_cepat']  , outRight['stop']))
    

    pioneer_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9]) #,rule10,rule11,rule12
    pioneer = ctrl.ControlSystemSimulation(pioneer_ctrl)
    return pioneer


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~My Program Start From Here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
#Remote API Configuration
vrep.simxFinish(-1) 
clientID=vrep.simxStart ('127.0.0.1',19997,True,True,5000,5)
if clientID!=-1:
    print ("Connected to remote API server") 
    vrep.simxAddStatusbarMessage(clientID,"Program Loaded!",vrep.simx_opmode_oneshot)  
else: 
    print ("Connection not successful")
    sys.exit("Could not connect")
    
    
val_s=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

#braitenbegr (belok kiri = -1*braitenberL) (X) braitenbegr (belok kanan = -1*braitenberR) 
#braitenber basic

braitenbergR=[ -6, -4  , -3, -2]
braitenbergL=[  -3, -1.5   ,  -1, -5]

#braitenbergR=[ -0.8, -7  , -7, -0.8]
#braitenbergL=[  0.8,  7  ,  7 ,  0.8]

for x in range(0,18):
        err,signal=vrep.simxGetFloatSignal(clientID,'s'+str(x+1),vrep.simx_opmode_streaming)
        
fuzzy = fuzzy_config()
vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot_wait)



'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~My Loop Start From Here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''

while vrep.simxGetConnectionId(clientID) != -1:
    
    #Config sensor
    sens_read() 
    
    #Initial input sensor 
    sLeft   = val_s[2]
    sFront  = val_s[3]
    sFrontR = val_s[8]
    sRight  = val_s[9]
    
    #Basic Action 
    fuzzy.input['sensor_left']      = sLeft 
    fuzzy.input['sensor_leftfront'] = sFront
#    fuzzy.input['sensor_frontright']= sFrontR
#    fuzzy.input['sensor_right']     = sRight
         
    fuzzy.compute()
    
    #fuzzy value     
    #Initial input Output for Motor + You can add Braitenberg for Turning Robot 
    vl = (fuzzy.output['outputL']) 
    vr = (fuzzy.output['outputR'])   
        
    
    
    #fuzzy + braitenberg for additional turning
    vBrLeft=vl
    vBrRight=vr
    for i in range(0,4):
        vBrLeft=vBrLeft+(braitenbergL[i]*(1-val_s[i+4]))
        vBrRight=vBrRight+(braitenbergR[i]*(1-val_s[i+4]))
    
    
    
    forward(5+vBrLeft,5+vBrRight)
    












     
    #Debug Sensor 
    aa = round(sLeft,2)
    ab = round(sFront,2) 
    ac = round(sFrontR,2)
    ad = round(sRight,2)
    
    ae = round(vl,2)
    af = round(vr,2) 
    
    ag = round(vBrLeft,2)
    ah = round(vBrRight,2) 
    
    #    ae = (str(aa)+" "+str(ab)+" || "+str(ac)+" "+str(ad))
    #print(aa,ab,ac,ad," || ",ae,af," || ",ag,ah)
    #print(aa,ab," || ",ae,af," || ",ag,ah)
    print(aa,ab," || ",ae,af," || ",ag,ah)
       
        
    
    




    
        
    

    
        
    
    
    
    