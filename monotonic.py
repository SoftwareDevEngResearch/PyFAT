#------------------------------#
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from pathlib import Path

import monotonic_functions
#------------------------------#
                                                                                
def monotonic(input_dir, output_dir, legendvar,YS02var):
    """Takes in two directories: input location (where the data is) and output 
    location (where to save results) and performs data analysis for monotonic 
    test data. Returns material parameters and plots"""

    print("************************************")
    print("Running Monotonic Analysis")

    #Define in and out Directories, make new folder for output ...
    input_directory = input_dir
    output_directory = Path(output_dir,"Monotonic_Results")
    os.mkdir(output_directory)

    #Make the output directory name a string for use later on ...
    output_directory = str(output_directory) 
    
    #Make folder for the plots to be saved to ...
    plots_directory = Path(output_directory,"Plots")
    os.mkdir(plots_directory)
    plots_directory = str(plots_directory)
    
    #"Unpack" data files from input directory ...
    print("Reading Input Data Files...")
    mfiles = next(os.walk(input_directory))[2]
    nfiles = len(mfiles) #Number of files in directory
        
    #Initiate all output variables for iteration
    testnames = [] #Names of test files
    E = [] #Elastic Modulus
    Pos1 = [] #Starting Position
    Pos2 = [] #End Position
    Nom_Ext = [] #Nominal Extension (end-start)
    MaxLoad = [] #Maximum recorded load
    MaxStrain = [] #Maximum recorded axial strain
    Max_Trans = [] #Maximum recorded transverse strain
    v = [] #Poisson's Ratio
    True_Strength = [] #Ultimate true stress
    True_Ductility = [] #Maximum true strain
    Engr_FracStrength = [] #Engineering stress @ failure
    YS02 = [] #0.2% offset strength
    YE02 = [] #0.2% offset strain
    YE02_P = [] #0.2% offset % elong.
    YS =[] #Yield Strength
    YE = [] #Yield Strain
    RA = [] # %-Reduction-Area
    
    #These will be used later to collect all data for 
    # overlaid stress vs strain plot ...
    totalstress = []
    totalstrain = []
    
    #Main Monotonic Analysis Loop...
    for j in range(nfiles):
        #Add each file name to the end of the directory location
        location = Path(input_directory, mfiles[j])
       
        filename = str(mfiles[j])
        filename = filename[0:-4]
        print("    Reading File ",filename)

        #Read in the Data set from every test individually...
        mData = pd.read_csv(location,header=None) 
        
        """
        This part (lines 80-96) will need improvement - I do not want the data 
        column #'s hard-coded. Instead, I want them automatically determined by
        the program.....
        """
        #Define Sample Geometry (width and thickness)...
        #Some systems will not need this step - automatically calc. stress
        w = mData[10]
        t = mData[11]
        w = w[0]
        t = t[0]
        Axial_GL = 50 #mm - gauge length of axial extensometer used...
        Trans_GL = w  #mm
        Thick_GL = t  #mm
        #
        #Define which channels are in which columns...
        Time = mData[0]      #Time in Seconds
        Position = mData[6]  #mm (from load frame)
        Load = mData[7]      #kN (from load cell)
        Ax_Ext = mData[8]    #% (axial extensometer)
        Trans_Ext = mData[9] #% (Transverse Extensometer)
        #        
        #Necessary Unit Conversions for Analysis...
        w = w/1000                #mm to m
        t = t/1000                #mm to m
        Position = Position/1000  #mm to m
        Load = Load*1000          #kN to N
        Axial_GL = Axial_GL/1000  #mm to m
        Trans_GL = Trans_GL/1000  #mm to m
        Thick_GL = Thick_GL/1000  #mm to m
        Ax_Str = Ax_Ext/100       #% to m/m
        Trans_Str = Trans_Ext/100 #% to m/m
        #        
        #Some Calculated Items...
        A0 = w*t #m^2 - original area
        extension = Ax_Str*Axial_GL #Axial Extension (m)
        Trans_mov = Trans_Str*Trans_GL #Transverse change (m)
        Thick_mov = Trans_Str*Thick_GL #THickness change (m)
        wi = w - Trans_mov #Instantaneous width
        ti = t - Thick_mov #Instantaneous thickness
        CS = wi*ti #Instantaneous cross-section
        #        
        #Cut off data at the max of axial strain...
        """ 
        Sometimes the extensometer slips at failure and reads a decrease in 
        strain... we do not want to include this in the analysis so the strain
        channel (and all other data) is cut off at the index where the maximum 
        axial strain occurs
        """
        max_str = max(Ax_Str)
        #returns list containing the index where max_str occurs
        endofdata = np.where(Ax_Str==max_str) 
        #Pull index out of the list...
        endofdata = endofdata[-1][0]
        #Trim all of the data channels...
        Time = Time[:endofdata]
        Load = Load[:endofdata]
        Position = Position[:endofdata]
        Ax_Str = Ax_Str[:endofdata]
        Trans_Str = Trans_Str[:endofdata]
        CS = CS[:endofdata]
        extension = extension[:endofdata]
        #        
        #Define Engineering Stress & Strain...
        Eng_S = Load/A0 #Pa - Load / Area
        Eng_E = Ax_Str #m/m - Axial Extensometer reading
        #        
        #Calculate True stress & strain ...
        True_S = Eng_S * (1 + Eng_E) #Pa
        True_E = np.log(1 + Eng_E)   #m/m
        #              
        """
        Now the data is set-up and redy for analysis...
        """
        #Get Start and end position...
        p1 = Position[0]*1000 #Starting position
        p2 = Position[len(Position)-1]*1000 #End position
        ext = p2-p1 #Nominal Extension (difference)
        #        
        #Max Load (kN)
        maxload = max(Load)
        maxload = maxload/1000 #N to kN
        #        
        #Max Axial Strain (%)
        maxstrain = max(Eng_E)
        maxstrain = maxstrain*100 #from m/m to %
        #        
        #Max Transverse Strain (%)
        maxtrans = max(Trans_Str)
        maxtrans = maxtrans*100 #from m/m to %
        #        
        #Get Poissons Ratio and Elastic Modulus...
        v_ratio, elastic_mod = monotonic_functions.elastic_params(
                Eng_E,Eng_S,Trans_Str
        )
        #
        #Get True Strength/Ductility...
        truestrength = max(True_S)
        truestrength = truestrength*10**-6 #convert Pa to MPa
        trueduct = max(True_E)
        #    
        #Get Engineering Fracture Strength...
        engfrac = Eng_S[len(Eng_S)-1]
        engfrac = engfrac*10**-6 #Convert to MPa
        #        
        #Get Yield Stress and Strain (Polymer yield criteria - 1st zero slope)
        yieldstress, yieldstrain = monotonic_functions.yield_point(
                Eng_E,Eng_S
        )
        #
        # ========================= START WORK HERE ========================== #
        """"   
        Need to automate the process for determining if the 0.2% offset is valid
        so the YS02var is not needed...
        This variable is a manual on/off switch for when this script was used in
        a GUI...
        """    
        #Get 0.2% Offset Stress and Strain
        if str(YS02var) == "1":
            intercept = -0.002*elastic_mod*10**9
            slope = elastic_mod*10**9
            intline = (slope*Eng_E) + intercept
            difference = abs(Eng_S - intline)
            #IF THE SCRIPT FAILS, try changing this parameter (e.g. try "<=10000")
            SUB3 = np.where(difference <= 1000000) 
            SUB3 = SUB3[-1][-1]
            offsetE = Eng_E[SUB3]
            perc_offsetE = offsetE*100
            offsetS = Eng_S[SUB3]
            offsetS = offsetS*10**-6 #Convert to MPa
        # 
        #Percent Reduction in area
        #ra = ((A0 - min(CS))/A0)*100
        ra = max(Trans_Str)*100 #CHECK THE MATH FOR THIS!!!!
        #       
        #-------------------Store Parameters------------------#
        testnames.append(filename)
        Pos1.append(p1)
        Pos2.append(p2)
        Nom_Ext.append(ext)
        MaxLoad.append(maxload)
        MaxStrain.append(maxstrain)
        Max_Trans.append(maxtrans) 
        v.append(v_ratio)  #Poisson's Ratio
        True_Strength.append(truestrength) 
        True_Ductility.append(trueduct)
        Engr_FracStrength.append(engfrac)
        YS.append(yieldstress*10**-6) #Yield Strength
        YE.append(yieldstrain)  #Yield Strain
        RA.append(ra)  # %-Reduction-Area
        E.append(elastic_mod)
        if str(YS02var) == "1":
            YS02.append(offsetS)  #0.2% offset strength
            YE02.append(offsetE)  #0.2% offset strain
            YE02_P.append(perc_offsetE) #%elong. @ 0.2% offset
        elif str(YS02var) == "0":
            YS02.append("N/A")  #0.2% offset strength
            YE02.append("N/A")  #0.2% offset strain
            YE02_P.append("N/A") #%elong. @ 0.2% offset
        #----------------------------------------------------#
#        
        #Plot of Stress vs. Strain for every test
        plt.figure()
        font = {'fontname':'Times New Roman'}
        plt.plot(Eng_E*100,Eng_S*10**-6)
        plt.plot(True_E*100,True_S*10**-6)
        plt.title('Stress vs. Strain - Monotonic ' + str(filename),fontdict = font)
        plt.xlabel('Strain (%)',fontdict = font)
        plt.ylabel('Stress (MPa)',fontdict = font)
        plt.grid(True)
        plt.legend(["Engineering Stress-Strain","True Stress-Strain"],loc=4)
        plt.savefig(plots_dir_png + '/Mono_Test_' + str(filename) + '.png')
        plt.savefig(plots_dir_pdf + '/Mono_Test_' + str(filename) + '.pdf')
#        
        #collects all stress-strain data for every test to plot on a single fig
        totalstress.append(Eng_S*10**-6)
        totalstrain.append(Eng_E*100)
    
    print("Writing Data...")    
    #Write all data to a .csv file
    with open((out_dir + '/Monotonic_Output.csv'),'w', newline='') as f:
        thewriter = csv.writer(f,delimiter=',')
        thewriter.writerow(['Test ID','Start Position (mm)','End Position (mm)','Nominal Extension(mm)',\
                            'Max Load (kN)','Max Axial Strain (%)','Max Transverse Strain (%)',\
                           'Poissons Ratio','Ult. True Strength (MPa)','Ult. True Ductility (m/m)',\
                           'Engineering Fracture Strength (MPa)','Yield Stress (MPa)',\
                           'Yield Strain(m/m)','Percent Area Red. (%)',\
                           'Elastic Modulus (GPa)','0.2% Offset Strength (MPa)',\
                           '0.2% Offset Strain (m/m)','0.2% offset % Elong.'])
#        
        #While loop is ised to write the variables for every test file separately
        count = 0
        maxcount = len(testnames)
#        
        while count < maxcount:
            thewriter.writerow((testnames[count],Pos1[count],Pos2[count],Nom_Ext[count],\
                                MaxLoad[count], MaxStrain[count], Max_Trans[count],v[count],\
                                True_Strength[count],True_Ductility[count],\
                               Engr_FracStrength[count],YS[count],YE[count],\
                               RA[count],E[count],YS02[count],YE02[count],YE02_P[count]))
            count = count + 1
#            
        thewriter.writerow(["_","Avg.","Avg.","Avg.","Avg.","Avg.","Avg.","Avg.",\
                            "Avg.","Avg.","Avg.","Avg.","Avg.","Avg.","Avg.",\
                            "Avg.","Avg.","Avg."])
        if str(YS02var) == "1":
            thewriter.writerow(["_",np.mean(Pos1),np.mean(Pos2),np.mean(Nom_Ext),\
                                np.mean(MaxLoad),np.mean(MaxStrain), np.mean(Max_Trans),\
                                np.mean(v),np.mean(True_Strength),np.mean(True_Ductility),\
                               np.mean(Engr_FracStrength),np.mean(YS),np.mean(YE), \
                               np.mean(RA),np.mean(E),np.mean(YS02),np.mean(YE02),\
                               np.mean(YE02_P)])
        elif str(YS02var) == "0":
             thewriter.writerow(["_",np.mean(Pos1),np.mean(Pos2),np.mean(Nom_Ext),\
                                np.mean(MaxLoad),np.mean(MaxStrain), np.mean(Max_Trans),\
                                np.mean(v),np.mean(True_Strength),np.mean(True_Ductility),\
                               np.mean(Engr_FracStrength),np.mean(YS),np.mean(YE), \
                               np.mean(RA),np.mean(E),"_","_","_"])
#    
    print("Creating Plots...")
    #Plot all stress vs strain on one figure
    font = {'fontname':'Times New Roman'}
    #If user chooses to add a legend ...
    if str(legendvar) == "1":
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for p in range(nfiles):
            ax.plot(totalstrain[p],totalstress[p],label=testnames[p])
        handles, labels = ax.get_legend_handles_labels() 
        lgd = ax.legend(handles, labels,loc=2,bbox_to_anchor=(1,1))
        ax.set_title('Stress vs. Strain (All Tests)',fontdict = font)
        ax.grid('on')
        ax.set_xlabel('Strain (%)',fontdict = font)
        ax.set_ylabel('Stress (MPa)',fontdict = font)
        fig.savefig(plots_dir_png + '/Stress_vs_Strain_All.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
        fig.savefig(plots_dir_pdf + '/Stress_vs_Strain_All.pdf',bbox_extra_artists=(lgd,), bbox_inches='tight')
    #If user does not choose to add a legend ...
    else:
        plt.figure()
        for p in range(nfiles):
            plt.plot(totalstrain[p],totalstress[p])
        plt.title('Stress vs. Strain (All Tests)',fontdict = font)
        plt.xlabel('Strain (%)',fontdict = font)
        plt.ylabel('Stress (MPa)',fontdict = font)
        plt.grid(True)
        plt.savefig(plots_dir_png + '/Stress_vs_Strain_All.png')
        plt.savefig(plots_dir_pdf + '/Stress_vs_Strain_All.pdf')

     #
    print("Finished.")
    print("************************************")
#------------------------------------------------------------------------------
# K. Gahan, 2019
   
    
    #