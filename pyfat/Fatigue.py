#------------------------------#
import os
import numpy as np
import pandas as pd
import csv
from pathlib import Path
#---------#
import plots
#------------------------------#
#
class Fatigue:
    """Takes in fatigue test data and performs necessary processing
    """
    
    def __init__(self, channels, stress_bool, geo_bool, modulus, file):
        """Initializes analysis for a single file with data channels defined
        """
        
        def get_HLC():
            """Uses cycle count channel to determine the closest recorded cycle
            to the exact half-life cycle. Returns the index of the closest 
            half-life cycle (HLC)"""
            
            #Determine exact HLC...
            total_cycles = max(self.cycles)
            HLC_exact = round(total_cycles/2)

            #Find closest recorded cycle...
            diff = []
            for cycle in self.cycles:
                difference = abs(cycle - HLC_exact)
                diff.append(difference)

            #Get index of closest recorded cycle...
            i = 0
            for difference in diff:
                if difference == min(diff):
                    index = i
                    break
                i += 1
            
            return index
        
        #Get Data and cycles channel and elastic modulus
        self.data = pd.read_csv(file,header=0)
        self.cycles = self.data[channels[0]]
        self.modulus = modulus*10**6 #MPa to Pa

        #Determined Half-Life Cycle index...
        HLC_index = get_HLC()

        #Pull out all data channels at HLC...
        self.max_load = self.data[channels[1]][HLC_index]*1000  #kN to N
        self.min_load = self.data[channels[2]][HLC_index]*1000  #kN to N
        self.max_strain = self.data[channels[3]][HLC_index]/100 #% to m/m
        self.min_strain = self.data[channels[4]][HLC_index]/100 #% to m/m

        #Get stress or geometry...
        if stress_bool:
            self.max_stress = self.data[channels[5]][HLC_index]*10**6 #MPa to Pa
            self.min_stress = self.data[channels[6]][HLC_index]*10**6 #MPa to Pa

        elif geo_bool:
            self.width = self.data[channels[5]][0]/1000     #mm to m
            self.thickness = self.data[channels[6]][0]/1000 #mm to m
            self.max_stress = self.max_load/(self.width * self.thickness) #Pa
            self.min_stress = self.min_load/self.width * self.thickness) #Pa

    
    def get_true_stress(self):
        """Uses engr max and min stress (self) to return true 
        max and min stress"""
        max_true_stress = self.max_stress*(1 + self.max_strain)
        min_true_stress = self.min_stress*(1 + self.min_strain)

        return max_true_stress, min_true_stress

    def get_true_strain(self):
        """Uses engr max and min strain (self) to return true 
        max and min strain"""
        max_true_strain = np.log(1 + self.max_strain)
        min_true_strain = np.log(1 + self.min_strain)
        return max_true_strain, min_true_strain

    def calc_strains(self, max_stress, min_stress, max_strain, min_strain):
        """Uses max/min true stress and strain and elastic modulus to 
        calculate max/min elastic and plastic strain"""

        #Get elastic strains...
        max_elastic = max_stress/self.modulus
        min_elastic = min_stress/self.modulus

        #Get plastic strains...
        max_plastic = max_strain - max_elastic
        min_plastic = min_strain - min_elastic

        return max_plastic, min_plastic, max_elastic, min_elastic



def data_fit(x_in, y_in):
    """Takes in an x (parameter) and a y (cycles or rev.) and performs data 
    fitting operations for power fxn. Returns a coefficient, exponent and 
    standard error"""
    x = np.log10(x_in)
    y = np.log10(y_in)
    xbar = np.mean(x)
    ybar = np.mean(y)

    #Get Estimator Values
    bhat = sum((x - xbar)*(y - ybar))/sum((x-xbar)**2)
    ahat = ybar - bhat*xbar
    yhat = ahat + (bhat*x)
    sigmasq = sum((y - yhat)**2)/(k-2)
    sigma = np.sqrt(sigmasq)

    #Get Standard Error and Strain-Life Parameters
    SE = sigma/np.sqrt(len(x_in))
    exponent = 1/bhat
    coefficient = (10**(ahat/-bhat))*((1/2)**c)

    return coefficient, expoennt, SE


def fatigue_analysis(
    input_dir, output_folder, files, channels, stress_bool, geo_bool, modulus
    ):

    print("Beginning Analysis Iteration...")
    runs = []
    names = []
    stress_amps = []
    strain_amps = []
    cycles = []

    for filename in files:
        this_file = Path(input_dir,filename)
        name = str(filename)
        print("    Reading File ",name)

        #Create Instance...
        run = Fatigue(
            channels, stress_bool, geo_bool, modulus, this_file
        )

        #Get true stress and strain...
        max_true_stress, min_true_stress = run.get_true_stress()
        max_true_strain, min_true_strain = run.get_true_strain()

        #Get Elastic and Plastic strain...
        max_plastic, min_plastic, max_elastic, min_elastic = run.calc_strains(
            max_true_stress, min_true_stress, max_true_strain, min_true_strain
        )

        #Calculate amplitudes and ranges etc...
        #stress range and amplitude
        stress_range = max_true_stress - min_true_stress
        stress_amp = stress_range/2
        #Plastic and Elastic strain amplitudes
        elastic_amp = (max_elastic - min_elastic)/2
        plastic_amp = (max_plastic - min_plastic)/2





