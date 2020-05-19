#------------------------------#
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from pathlib import Path
#------------------------------#
#
class Monotonic:
    """Takes in monotonic (tensile test) data and performs necessary processing
    """
    def __init__(self, channels, stress_bool, geo_bool, file):
        """Initializes analysis for a single file with data channels defined
        """
        self.data = pd.read_csv(file,header=0)

        #Define axial strain...
        self.ax_str = self.data[channels[2]]/100    #% to m/m
        #Get max strain, cut off all data at that index ("eod")...
        max_ax_str = max(self.ax_str)
        eod = np.where(self.ax_str == max_ax_str)[-1][0]

        self.position = self.data[channels[0]][:eod]/1000 #mm to m
        self.load = self.data[channels[1]][:eod]*1000     #kN to N
        self.ax_str = self.data[channels[2]][:eod]/100    #% to m/m
        self.tr_str = self.data[channels[3]][:eod]/100    #% to m/m

        if stress_bool:
            self.stress = self.data[channels[4]][:eod]
        elif geo_bool:
            self.width = self.data[channels[4]][0]/1000         #mm to m
            self.thickness = self.data[channels[5]][0]/1000     #mm to m
            self.stress = self.load/(self.width*self.thickness) #Pa


    def get_true(self):
        """Takes in engineering stress and strain channels, returns true stress 
        and strain channels"""
        true_stress = self.stress*(1 + self.ax_str)
        true_strain = np.log(1 + self.ax_str)
        return true_stress, true_strain


    def get_modulus_and_poissons(self):
        """Uses axial strain, transverse strain, and engr stress to determine 
        Poisson's ratio in the range of 0.0005-0.0025 axial strain, and the
        elastic (tensile) modulus within 0.00125-0.0025 axial strain"""
        tr_str = self.tr_str
        ax_str = self.ax_str
        stress = self.stress
        diff1 = abs(ax_str - 0.0005)
        diff2 = abs(ax_str - 0.0025)
        SUB1 = np.where(diff1 < 0.0001)[-1][-1]   
        SUB2 = np.where(diff2 < 0.0001)[-1][-1] 
        SUB12 = round((SUB1/2),0)
        v_ratio = (
            (tr_str[SUB2] - tr_str[SUB1])/(ax_str[SUB2] - ax_str[SUB1])
        )
        e_mod = (
            (stress[SUB2] - stress[SUB12])/(ax_str[SUB2] - ax_str[SUB12])
        )
        return v_ratio, e_mod


    def get_offset(self,modulus):
        """Draws a 0.2% offfset line with slope equivalent to elastic 
        modulus, finds intersection point (0.2% offset stress/strain point)"""
        #Create intercept line...
        intercept = -0.002*modulus
        slope = modulus
        intline = (slope*self.ax_str) + intercept

        #Diff. bet. intercept line and stress-strain curve...
        difference = abs(self.stress - intline)

        try:
            #Find where diff. gets small -> Intercept location
            SUB = np.where(difference <= 10**5)[-1][-1] 
            offset_strain = self.ax_str[SUB]
            offset_stress = self.stress[SUB]
        except:
            offset_strain = None
            offset_stress = None
            print("     -- Error with 0.2 percent offset method (skipped) --")

        return offset_strain, offset_stress


    def get_yield(self):
        """Gets yield point (as defined for plastic materials) as the max
        of engineering stress and the strain at that same point."""
        yield_stress = max(self.stress)
        SUB = np.where(self.stress == yield_stress)[-1][-1]
        yield_strain = self.ax_str[SUB]
        max_load = self.load[SUB]

        return yield_stress, yield_strain, max_load


    def 

    def get_max_values(self):
        """Returns max values for axial engr strain, engineering stress, 
        load, and s
        """
        pass




    """
    def get_pr(self): 
        emod = self.get_emod()

    
    def get_stress(self,stress_bool,geo_bool):
        if stress_bool:
            stress = self.stress
        elif geo_bool:
            w = self.width[0]
            t = self.width[0]
            area = w*t
            stress = self.load/area
        return stress
    """ 

        

def mono_analysis(
    input_dir, output_dir, files, channels, stress_bool, geo_bool
    ):

    print("Beginning Analysis Iteration...")
    for filename in files:
        this_file = Path(input_dir,filename)
        name = str(filename)
        print("    Reading File ",name)

        #Create Instance...
        run = Monotonic(
            channels, stress_bool, geo_bool, this_file
        )
        
        #Get true stress and strain
        true_stress, true_strain = run.get_true()

        #Get elastic modulus and Poissons ratio...
        poissons, emod = run.get_modulus_and_poissons()

        #get 0.2% offset strain and stress
        offset_strain, offset_stress = run.get_offset(emod)

        #Get yield point(max of stress-strain curve)
        yield_stress, yield_strain, max_load = run.get_yield()

        
        








    


