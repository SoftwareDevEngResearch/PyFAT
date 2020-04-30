"""
This script contains functions to perform some of the major analysis procedures
within the monotonic analysis script (monotonic.py)
"""
#------------------------------#
import numpy as np
#------------------------------#

def elastic_params(engr_strain,engr_stress,trans_strain):
    """
    Calculates Poisson's ratio (v) by finding the change in transverse strain 
    divided by the change in axial strain in the region of 0.0005 to 0.0025 
    axial strain.
    Calculates Elastic modulus (E) (or Modulus of elasticity or tensile modulus)
    by finding the slope of engineering stress vs strain in the region of 0.0001 
    to 0.00125 strain.
    """
    #Determine index where the strain is equal to 0.0005 and 0.0025...
    diff1 = abs(engr_strain - 0.0005)
    diff2 = abs(engr_strain- 0.0025)
    #SUB1 and SUB2 are the indexes...
    SUB1 = np.where(diff1 < 0.0001)   
    SUB2 = np.where(diff2 < 0.0001)   
    SUB1 = SUB1[-1][-1]
    SUB2 = SUB2[-1][-1]
    #Calculate index for 0.00125...
    MID = round((SUB1/2),0)
    #Calculate parameters...
    v = (trans_strain[SUB2] - trans_strain[SUB1])/\
        (engr_strain[SUB2] - engr_strain[SUB1])
    E = (Eng_S[SUB2] - Eng_S[MID])/(Eng_E[SUB2] - Eng_E[MID])
    E = E*10**-9 #convert Pa to GPa
    return v, E

def yield_point(engr_strain,engr_stress):
    """
    Calculates the yield point according to the definition of yield for a
    polymer... First point where increase in strain causes 0 increase in stress
    (Max stress vs strain)
    """
    yieldstress = max(engr_strain) #yield stress (Pa)
    #Get index of max stress...
    ysindex = np.where(Eng_S==yieldstress) 
    ysindex = ysindex[-1][-1]
    yieldstrain = Eng_E[ysindex] #yield strain (m/m)
    return yieldstress, yieldstrain





