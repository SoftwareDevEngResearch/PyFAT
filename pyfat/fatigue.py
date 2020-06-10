#------------------------------#
import os
import numpy as np
import pandas as pd
import csv
from pathlib import Path
#---------#
import plots
#------------------------------#

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
        self.modulus = int(modulus)*10**6 #MPa to Pa

        #Determined Half-Life Cycle index...
        HLC_index = get_HLC()
        self.HLC = HLC_index

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
            self.min_stress = self.min_load/(self.width * self.thickness) #Pa

    
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
        modulus = self.modulus #Elastic Modulus in Pa

        #Get elastic strains...
        max_elastic = max_stress/modulus
        min_elastic = min_stress/modulus

        #Get plastic strains...
        max_plastic = max_strain - max_elastic
        min_plastic = min_strain - min_elastic

        return max_plastic, min_plastic, max_elastic, min_elastic

#==============================================================================#


def data_fit(x_in, y_in):
    """Takes in an x (parameter) and a y (cycles or rev.) and performs data 
    fitting operations for power fxn. Returns a coefficient, exponent and 
    standard error"""
    if len(x_in) != len(y_in):
        raise AttributeError(
            "Cannot perform fitting: data are not the same length"
            )
    else:
        k = len(x_in)

    #Convert Data to list for analysis
    i = 0
    x_list = []
    y_list = []
    for i in range(k):
        x_list.append(x_in[i])
        y_list.append(y_in[i])
        i += 1

    x = np.log10(x_list)
    y = np.log10(y_list)
    xbar = np.mean(x)
    ybar = np.mean(y)

    #Get Estimator Values
    bhat = sum((x - xbar)*(y - ybar))/sum((x-xbar)**2)
    ahat = ybar - bhat*xbar
    yhat = ahat + (bhat*x)
    sigmasq = sum((y - yhat)**2)/(k-2)
    sigma = np.sqrt(sigmasq)

    #Get Standard Error and fatigue Parameters
    SE = sigma/np.sqrt(len(x_in))
    exponent = 1/bhat
    coefficient = (10**(ahat/-bhat))*((1/2)**exponent)

    return coefficient, exponent, SE


def trim_data(output_dir):
    """Reads in HLC data from the written csv file, removes 
    neg. plastic strain tests and runout tests, returns dataframe with 
    trimmed data"""
    #Read File...
    HLC_file = Path(output_dir,'HalfLifeData.csv')
    HLC_data = pd.read_csv(HLC_file)

    #Define Data...
    name = HLC_data['FileName']
    Cycf = HLC_data['MaxCycles']
    stress_range = HLC_data['StressRange']
    stress_amp = HLC_data['StressAmp']
    strain_amp = HLC_data['StrainAmp']
    elastic_amp = HLC_data['ElasticAmp']
    plastic_amp = HLC_data['PlasticAmp']

    #Take out Neg. Plastic strain and runout tests...
    num_vals = range(len(plastic_amp))

    for i in num_vals:

        if plastic_amp[i] <= 0.0:
            print(
                "-Note- File {} skipped (neg. plastic strain)".format(name[i])
                )
            del stress_range[i], stress_amp[i], strain_amp[i], elastic_amp[i],\
                plastic_amp[i], Cycf[i], name[i]

        elif Cycf[i] == 2000000:
            print(
                "-Note- File {} skipped (runout test)".format(name[i])
                )
            del stress_range[i], stress_amp[i], strain_amp[i], elastic_amp[i],\
                plastic_amp[i], Cycf[i], name[i]

    #Create dataframe for trimmed data
    trimmed_data = pd.DataFrame(np.array([name, Cycf, stress_range, stress_amp, 
        strain_amp, elastic_amp, plastic_amp]).transpose(), 
        columns=['FileName','MaxCycles','StressRange','StressAmp','StrainAmp',
            'ElasticAmp', 'PlasticAmp']
    )

    return trimmed_data, HLC_data


def get_results(output_dir, date, time):
    """Reads in HLC data from the written csv file, performs data fitting,
    writes material parameters"""

    #Trim data for neg. plastic strain and runout tests...
    data, data_original = trim_data(output_dir)

    print("Fitting Data...")
    #Fit Elastic Strain-Life...
    fat_str_coeff, fat_str_exp, SEe = data_fit(
        data['StressAmp'], data['MaxCycles']
    )

    #Fit Plastic Strain-Life...
    fat_duct_coeff, fat_duct_exp, SEp = data_fit(
        data['PlasticAmp'], data['MaxCycles']
    )

    #Fit Stress-Life...
    SRI1, b1, SEs = data_fit(
        data['StressRange'], data['MaxCycles']
    )

    #Save Fatigue Results to a log file...
    print("Saving Results...")
    output_file = Path(output_dir,"FatigueResults.log") 

    with open(output_file,'w', newline='') as f:
        f.write(
            "Fatigue Results: Analysis " + date + "_" + time + "\n"
            "--------------------------------------------\n"
            "Strain-Life:\n"
            "Fatigue Strength Coefficient (MPa): " +\
                 str(round((fat_str_coeff*10**-6),4)) + "\n"
            "Fatigue Strength Exponent:          " +\
                 str(round(fat_str_exp,5)) + "\n"
            "Elastic Standard Error (SEe):       " +\
                 str(round(SEe,4)) + "\n"
            "Fatigue Ductility Coefficient:      " +\
                 str(round(fat_duct_coeff,5)) + "\n"
            "Fatigue Ductility Exponent:         " +\
                 str(round(fat_duct_exp,5)) + "\n"
            "Plastic Standard Error (SEp):       " +\
                 str(round(SEp,4)) + "\n"
            "--------------------------------------------\n"
            "Stress-Life:\n"
            "Stress-Range Intercept (MPa):       " +\
                 str(round((SRI1*10**-6),4)) + "\n"
            "Stress-Life Exponent (b1):          " +\
                 str(round(b1,5)) + "\n"
            "Stress-Life Standard Error (SEs):   " +\
                 str(round(SEs,4)) + "\n"
            "--------------------------------------------\n"
            )

    results = [
        fat_str_coeff, fat_str_exp, SEe, fat_duct_coeff, fat_duct_exp, SEp,
        SRI1, b1, SEs
    ]

    return results, data_original
    

def create_plots(data, results, modulus, output_dir):
    print("Creating Plots...")

    save_loc = Path(output_dir, "plots")
    modulus = int(modulus)*10**6

    #Create Models...
    N = 2000000
    Nf = np.linspace(1,N,N) #Cycles to Failure Variable
    Rf = 2*Nf #Reversals to Failure Variable
    plastic_SL = (results[3]*(Rf**results[4])) #Plastic Strain-Life
    elastic_SL = ((results[0]/modulus)*(Rf**results[1])) #Elastic Strain-Life
    total_SL = plastic_SL + elastic_SL #Total Strain-Life
    stresslife = (results[6]*(Nf**results[7])) #Stress-Life

    #Plot Plastic Strain-Life...
    plots.Plots(None, save_loc).fatigue_loglog(
        data['MaxCycles'], data['PlasticAmp'], Rf, plastic_SL, "P"
    )

    #Plot Elastic Strain-Life...
    plots.Plots(None, save_loc).fatigue_loglog(
        data['MaxCycles'], data['ElasticAmp'], Rf, elastic_SL, "E"
    )

    #Plot Stress-Life...
    c = 10**-6
    plots.Plots(None, save_loc).fatigue_loglog(
        data['MaxCycles'], data['StressRange']*c, Nf, stresslife*c, "S"
    )

    #Plot Strain Amp vs Cycles...
    StrainLife = total_SL*100
    plots.Plots(None,save_loc).fatigue_semilogX(
        data['MaxCycles'], data['StrainAmp']*100, Nf, StrainLife
    )

    #Plot total strain-life 
    plots.Plots(None,save_loc).total_strain_life(
        Nf, plastic_SL, elastic_SL, total_SL
    )



def fatigue_analysis(
    input_dir, output_dir, files, channels, stress_bool, geo_bool, modulus,
    date, time
    ):

    #Write Half-life data to csv file...
    with open((str(output_dir) + '/HalfLifeData.csv'),'w', newline='') as f:
        thewriter = csv.writer(f,delimiter=',')
        thewriter.writerow(['FileName','MaxCycles','StressRange','StressAmp',
            'StrainAmp','ElasticAmp','PlasticAmp'])

        print("Beginning Analysis Iteration...")

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
            #Plastic and Elastic and total strain amplitudes
            elastic_amp = (max_elastic - min_elastic)/2
            plastic_amp = (max_plastic - min_plastic)/2
            total_strain_amp = (max_true_strain - min_true_strain)/2

            #Get cycles to failure
            max_cycles = max(run.cycles)

            #Write Data to Half-Life csv file...
            thewriter.writerow([
                name, max_cycles, stress_range, stress_amp, total_strain_amp,
                elastic_amp, plastic_amp
            ])

    #Get results...
    results, data_original = get_results(output_dir, date, time)

    #Create plots...
    create_plots(data_original, results, modulus, output_dir)
