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
class Monotonic:
    """Takes in monotonic (tensile test) data and performs necessary processing
    """
    def __init__(self, channels, stress_bool, geo_bool, file):
        """Initializes analysis for a single file with data channels defined
        """
        self.data = pd.read_csv(file,header=0)

        #Define axial strain...
        strain = self.data[channels[2]]/100    #% to m/m
        #Get max strain, cut off all data at that index ("eod")...
        max_strain = max(strain)
        eod = np.where(strain == max_strain)[-1][0]

        self.position = self.data[channels[0]][:eod]/1000 #mm to m
        self.load = self.data[channels[1]][:eod]*1000     #kN to N
        self.ax_str = self.data[channels[2]][:eod]/100    #% to m/m
        self.tr_str = self.data[channels[3]][:eod]/100    #% to m/m

        if stress_bool:
            self.stress = self.data[channels[4]][:eod]*10**6    #MPa to Pa
        elif geo_bool:
            self.width = self.data[channels[4]][0]/1000         #mm to m
            self.thickness = self.data[channels[5]][0]/1000     #mm to m
            self.stress = self.load/(self.width*self.thickness) #Pa


    def get_positions(self):
        """Finds start and end position as well as nominal extension"""
        p1 = self.position[0]               #Starting position
        p2 = self.position[len(self.position)-1] #End position
        ext = p2-p1                    #Nominal Extension
        return p1, p2, ext

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


    def get_engr_fracture(self):
        """defines fracture point stress, axial and trans. strain"""
        engr_frac_strength = self.stress[len(self.stress)-1]
        engr_frac_strain = max(self.ax_str)
        trans_frac_strain = max(self.tr_str)

        return engr_frac_strength, engr_frac_strain, trans_frac_strain


#==============================================================================#

def mono_analysis(
    input_dir, output_dir, files, channels, stress_bool, geo_bool
    ):

    with open((str(output_dir) + '/Monotonic_Output.csv'),'w', newline='') as f:
        thewriter = csv.writer(f,delimiter=',')
        thewriter.writerow([
            'File Name','Start Position (mm)','End Position (mm)',
            'Nominal Extension(mm)','Poissons Ratio','Tensile Modulus (GPa)',
            '0.2% Offset Strength (MPa)','0.2% Offset Strain (m/m)',
            'Max Load (kN)','Yield Stress (MPa)','Yield Strain(m/m)',
            'Ult. True Strength (MPa)','Engineering Fracture Strength (MPa)',
            'Ult. True Ductility (m/m)','Max Axial Strain (%)',
            'Max Transverse Strain (%)'
        ])

        print("Beginning Analysis Iteration...")
        runs = []
        names = []
        for filename in files:
            this_file = Path(input_dir,filename)
            name = str(filename)
            print("    Reading File ",name)

            #Create Instance...
            run = Monotonic(
                channels, stress_bool, geo_bool, this_file
            )

            #Get positions...
            p1, p2, ext = run.get_positions()

            #Get true stress and strain...
            true_stress, true_strain = run.get_true()

            #Get elastic modulus and Poissons ratio...
            poissons, emod = run.get_modulus_and_poissons()

            #get 0.2% offset strain and stress...
            offset_strain, offset_stress = run.get_offset(emod)

            #Get yield point(max of stress-strain curve)...
            yield_stress, yield_strain, max_load = run.get_yield()

            #Get fracture stress and strain...
            engr_frac_strength, max_ax_str, max_tr_str = run.get_engr_fracture()

            #Get ultimate true stress/strain...
            max_true_stress = max(true_stress)
            max_true_strain = max(true_strain)

            #Write values to file for each test...
            
            thewriter.writerow([
                name, p1, p2, ext, poissons, emod*10**-9, offset_stress*10**-6, 
                offset_strain,max_load/1000, yield_stress*10**-6, yield_strain, 
                max_true_stress*10**-6, engr_frac_strength*10**-6, 
                max_true_strain, max_ax_str*100, max_tr_str*100   
            ])

            #make Individual Test Plot...
            plots.Plots(
                name[:-4],Path(str(output_dir),'plots')
            ).mono_test_plot(
                run.ax_str,run.stress,true_strain,true_stress
            )

            runs.append(run)
            names.append(name[:-4])
        print("Saving Results...")
        
        #Plots...
        print("Creating Plots...")
        plots.Plots(
            name[:-4],Path(str(output_dir),'plots')
            ).mono_all_plot(runs,names)





        
