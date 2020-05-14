#------------------------------------------------------------------------------
##-----------------------Fatigue Analysis Function-----------------------------
#------------------------------------------------------------------------------
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys
from pathlib import Path
#
#
def Fatigue_anlys(input_dir,output_dir,tensile_modulus):
    #Define Directories, make new folders -------------------------------------
    folder_names = ["Fatigue_Results","plots","pdf","png"]
    
    #
    #For Fatigue Results
    out_dir = Path(output_dir,folder_names[0])
    os.mkdir(out_dir)
    out_dir = str(out_dir)
    #
    #For Plots (in new fatigue folder)
    plots_dir = Path(out_dir,folder_names[1])
    os.mkdir(plots_dir)
    plots_dir = str(plots_dir)
    #
    #separate by file type pdf or png
    type_dir1 = Path(plots_dir,folder_names[2])
    type_dir2 = Path(plots_dir,folder_names[3])
    os.mkdir(type_dir1)
    os.mkdir(type_dir2)
    pdf_dir = str(type_dir1)
    png_dir = str(type_dir2)
    
    #Get Data -----------------------------------------------------------------
    print("reading Data...")
    directory1 = input_dir
    files = next(os.walk(directory1))[2] #Pull Out .csv Files from directory
    numfiles = len(files)    
    #Get Input Modulus Value - convert from MPa to Pa
    E = tensile_modulus
    E = float(E)
    E = E*1e6  
#    
    #Initiate main variables
    S_Amplitude = []
    E_Amplitude = []
    E_Amplitude_Elastic = []
    E_Amplitude_Plastic = []
    Cyc_Fail = []  
    Avg_E_Amp = []
    S_Range = []
#
    print("Beginning Analysis Iteration...")
    #for loop is used t perform analysis on every daya file separately    
    for i in range(numfiles):
        #Add each file name to the end of the directory
        location = Path(directory1, files[i]) 
#        
        #Read in the Data file from every test individually
        Data = pd.read_csv(location, header = None)
#    
        #****Geometry Information****
        W = Data[10]         #Width (mm)
        T = Data[11]         #Thickness (mm)    
        W = W[0]
        T = T[0]
#    
        #****Define Data Sets****
        Pos = Data[6]        #Position (mm)
        Load = Data[7]       #Load (kN)
        Strain = Data[8]     #Axial Strain (%)
        AvgEamp = Data[12]   #Average Strain AMplitude (entire test)
        CtoF = Data[13]      #Cycles to Failure
        AvgEamp = AvgEamp[0]
        CtoF = CtoF[0]
#       
        #****Conversions****
        W = W/1000          #Width (m)
        T = T/1000          #Thickness (m)
        A = W*T          #Area
        Load = Load*1000    #Load (N)
        Pos = Pos/1000      #Position (m)
        Strain = Strain/100 #Axial Strain (m/m)
#        
        #****Engineering Values****
        Engr_S = Load/A #N/m^2 or Pa
        Engr_E = Strain #m/m
#        
        #****True Values****
        True_S = Engr_S * (1 + Engr_E) #Pa
        True_E = np.log(1 + Engr_E)   #m/m
#        
        #****Half-Life Values****
        Max_S = max(True_S) #Max True Stress
        Min_S = min(True_S) #Min True Stress
        Max_E = max(True_E) #Max True Strain
        Min_E = min(True_E) #Min True Strain   
#    
        stressrange = Max_S - Min_S
#        
        if CtoF == 1:
            S_Amp = Max_S #True S Amp is max S if one cycle
            E_Amp = Max_E #True E Amp is max E if one cycle
        else:
            S_Amp = (Max_S - Min_S)/2 #True Stress Amplitude if >1 cycle
            E_Amp = (Max_E - Min_E)/2 #True Strain Amplitude if >1 cycle
#        
        E_Amp_Elastic = S_Amp/E   #True Elastic Strain Amplitude
        E_Amp_Plastic = E_Amp - E_Amp_Elastic #True Plastic Strain Amplitude
#        
#        
        S_Amplitude.append(S_Amp*10**-6)
        E_Amplitude.append(E_Amp)
        E_Amplitude_Elastic.append(E_Amp_Elastic)
        E_Amplitude_Plastic.append(E_Amp_Plastic)    
        Cyc_Fail.append(CtoF)
        Avg_E_Amp.append(AvgEamp)
        S_Range.append(stressrange)
#        
    #****Print to .csv File****
    print("Writing Half-Life Data...")
    with open(out_dir + '/HysteresisData_Output.csv','w', newline='') as f:
        thewriter = csv.writer(f,delimiter=',')
        thewriter.writerow(['Cyc_F','Avg_E_Amp','S_Amp','S_Range','E_Amp',\
                            'E_AmpE','E_AmpP'])
        count = 0
        maxcount = len(S_Amplitude)
        #While loop is ised to write the variables for every test file separately        
        while count < maxcount:
            thewriter.writerow((Cyc_Fail[count],Avg_E_Amp[count],S_Amplitude[count],\
                                S_Range[count],E_Amplitude[count],\
                                E_Amplitude_Elastic[count], E_Amplitude_Plastic[count]))
            count = count + 1
    #==========================================================================
    #                        Fatigue Fitting Portion
    #==========================================================================
    print("The Fatigue Fitting Analysis is Running...")

#
#
    #Read In Hysteresis Data from Tests (output fule of Half-Life Analysis)
    HystData = pd.read_csv(out_dir +'/HysteresisData_Output.csv')
#   
    #Define Data Sets for Hysteresis
    Cycf = HystData.Cyc_F      #Cycles to Failure
    S_Amp = HystData.S_Amp     #Stress Amplitude (MPa)
    E_Amp = HystData.E_Amp     #Strain AMplitude (m/m)
    E_AmpE = HystData.E_AmpE   #Elastic Strain Amplitude
    E_AmpP = HystData.E_AmpP   #Plastic Strain Amplitude
    S_Rng = HystData.S_Range   #Stress Range (Pa)
    Average_E_Amp = HystData.Avg_E_Amp
#    
    S_Amp = (10**6)*S_Amp      #Convert MPa to Pa
    Rev_F = 2*Cycf             #2 reversals per cycle
#    
#    
    #Define Data Sets for E vs Nf
    Cycles = Cycf    #Cycles to Failure (N)
    Str_Amp = Average_E_Amp #Strain Amplitude (%)
#    
    #Exclude runout tests from regression fits (also any tests with <0 plastic strain)
    Cycf_fit = []
    E_AmpP_fit = []
    S_Amp_fit = []
    S_Rng_fit = []
    for k in range(len(Cycf)):
        if Cycf[k] < 2000000 and E_AmpP[k] > 0:
            Cycf_fit.append(Cycf[k])
            E_AmpP_fit.append(E_AmpP[k])
            S_Amp_fit.append(S_Amp[k])
            S_Rng_fit.append(S_Rng[k])            
    Cycf_fit = pd.Series(Cycf_fit)        
#    
#    
    numfiles = len(Cycf) #number of tests (data points)
#  
#----------------Fitting methods according to ASTM E739------------------------
    #t-distributuion values 95% confidence (if # data points is between 20-50)
    n_dof = numfiles - 2 #degrees of freedom
    if n_dof ==20:
        tp = 2.086
    elif 20<n_dof<30:
        tp = 2.021 - (((2.042-2.086)*(30-numfiles))/(30-20))
    elif n_dof == 30:
        tp = 2.042
    elif 30<n_dof<40:
        tp = 2.021 - (((2.021-2.042)*(40-numfiles))/(40-30))
    elif n_dof == 40:
        tp = 2.021
    elif 40<n_dof<50:
        tp = 2.009 - (((2.009-2.021)*(50-numfiles))/(50-40))
    elif n_dof == 50:
        tp = 2.009
    else:
        tp = 2.00
        old_stdout = sys.stdout
        log_file = open(out_dir + "/ERROR.log","w")
        sys.stdout = log_file  
        print("There was an Error in the Fatigue Fitting Operation:")
        print("         Arbitrary value used for tp (2.00). # Data points should (ideally) ")
        print("         be between 20 and 50")
        sys.stdout = old_stdout
        log_file.close()
#    
    #----Plastic Strain-Life----#
    #Define Plastic Strain-Life Data
    x = np.log10(E_AmpP_fit)
    y = np.log10(Cycf_fit)
    xbar = np.mean(x)
    ybar = np.mean(y)
    #Get Estimator Values
    bhat = sum((x - xbar)*(y - ybar))/sum((x-xbar)**2)
    ahat = ybar - bhat*xbar
    yhat = ahat + (bhat*x)
    sigmasq = sum((y - yhat)**2)/(k-2)
    sigma = np.sqrt(sigmasq)
    #Get Standard Error and Strain-Life Parameters
    SEp = sigma/np.sqrt(numfiles)
    c = 1/bhat
    epsf = (10**(ahat/-bhat))*((1/2)**c)
#    
    #----Elastic Strain-Life----#
    #Define Elastic Strain-Life Data
    x = np.log10(S_Amp_fit)
    y = np.log10(Cycf_fit)
    xbar = np.mean(x)
    ybar = np.mean(y)
    #Get Estimator Values
    bhat = sum((x - xbar)*(y - ybar))/sum((x-xbar)**2)
    ahat = ybar - bhat*xbar
    yhat = ahat + (bhat*x)
    sigmasq = sum((y - yhat)**2)/(k-2)
    sigma = np.sqrt(sigmasq)
    #Get Standard Error and Strain-Life Parameters
    SEe = sigma/np.sqrt(numfiles)
    b = 1/bhat
    sigf = (10**(ahat/-bhat))*((1/2)**b)
#    
    #----Cyclic Stress-Strain----#
    x = np.log10(S_Amp_fit)
    y = np.log10(E_AmpP_fit)
    xbar = np.mean(x)
    ybar = np.mean(y)
    #Get Estimator Values
    bhat = sum((x - xbar)*(y - ybar))/sum((x-xbar)**2)
    ahat = ybar - bhat*xbar
    yhat = ahat + (bhat*x)
    sigmasq = sum((y - yhat)**2)/(k-2)
    sigma = np.sqrt(sigmasq)
    #Get Standard Error 
    SEc = sigma/np.sqrt(numfiles)
    #Define (solve for) Cyclic Stress-Strain Curve
    nprime = b/c
    Kprime = sigf/(epsf**nprime)
#    
    #-------Stress-Life--------#
    x = np.log10(S_Rng_fit)
    y = np.log10(Cycf_fit)
    xbar = np.mean(x)
    ybar = np.mean(y)
    #Get Estimator Values
    bhat = sum((x - xbar)*(y - ybar))/sum((x-xbar)**2)
    ahat = ybar - bhat*xbar
    yhat = ahat + (bhat*x)
    sigmasq = sum((y - yhat)**2)/(k-2)
    sigma = np.sqrt(sigmasq)
    #Get Standard Error and Stress-Life Parameters
    SEs = sigma/np.sqrt(numfiles)
    b1 = 1/bhat
    SRI1 = (10**(ahat/-bhat)) 
#    
#---------------------------log file (fatigue results)-------------------------
    print("Writing and Saving Fatigue Parametrs...")
    old_stdout = sys.stdout
    log_file = open(out_dir + "/Fatigue_Results.log","w")
    sys.stdout = log_file
    print("--------------------------------------------------------------------")
    print("Strain-Life (R = -1)")
    print("Fatigue Ductility Coefficient (Ef'):    ",round(epsf,5))
    print("Fatigue Ductility Exponent (c):        ",round(c,5))
    print("Fatigue Strength Coefficient (Sf'):    ",round(sigf*10**-6,4),"MPa") 
    print("Fatigue Strength Exponent (b):         ",round(b,5))
    print("Plastic Standard Error (SEp):           ",round(SEp,4))
    print("Elastic Standard Error (SEe):           ",round(SEe,4))
    print("-------------------------------------------------")
    print("Cyclic Strength Coefficient (K'):     ",round(Kprime*10**-6,4),"MPa (calculated)")
    print("Cyclic Strain Hardening Exponent (n'):  ",round(nprime,4),"(calculated)")
    print("Cyclic Standard Error (SEc):            ",round(SEc,4))
    print("-------------------------------------------------")
    print("Stress-Life (R = -1)")
    print("Stress Range Intercept (SRI1):        ",round(SRI1*10**-6,4), "MPa")
    print("Stress-Life Slope 1 (b1):              ",round(b1,5))
    print("Stress-Life Standard Error (SEs):       ", round(SEs,4))
    print("--------------------------------------------------------------------")
    print("Number of Data Points:",numfiles)
    sys.stdout = old_stdout
    log_file.close()
#------------------------------------------------------------------------------
#    
#   
#   
#-------------------------------Create Models----------------------------------
    print("Creating E-N and S-N Models...")
    #E-N Model
    N = 2000000
    Nf = np.linspace(1,N,N) #Cycles to Failure Variable
    Rf = 2*Nf #Reversals to Failure Variable
    EP = (epsf*(Rf**c)) #Plastic Strain-Life
    EE = ((sigf/E)*(Rf**b)) #Elastic Strain-Life
    EN = EP + EE #Total Strain-Life
#    
    #Create S-N Model
    SN = SRI1*(Nf**b1)
#    
    #Cyclic stress-strain curve
    Ncyc = max(S_Amp)
    cycS_Amp =  np.linspace(0,Ncyc) 
    cycE_Amp = (cycS_Amp/E) + (cycS_Amp/Kprime)**(1/nprime)
#    
#---------------------------------Plotting-------------------------------------
    print("Creating Plots...")
    #Plot E vs N with data points
    plt.figure()
    plt.scatter(Cycles,Str_Amp,color = 'black')
    for i in range(len(Cycles)):
        if Cycles[i] == 2000000:
            plt.scatter(Cycles[i],Str_Amp[i],color = 'red')
    plt.plot(Nf,EN*100,'r--')
    plt.xscale('log')
    plt.grid(True,which="both",ls="--")
    plt.xlim((1,N))
    font = {'fontname':'Times New Roman'}
    plt.title("Strain Amplitude (%) vs Cycles to Failure",fontdict=font)
    plt.ylabel("Strain Amplitude (%)",fontdict=font)
    plt.xlabel("Cycles to Failure (N)",fontdict=font)
    plt.savefig(png_dir + '/Strain_vs_Cycles.png',bbox_inches='tight')
    plt.savefig(pdf_dir + '/Strain_vs_Cycles.pdf',bbox_inches='tight')
#    
    #Plot log-log E-N w/ plastic and elastic lines
    plt.figure()
    plt.loglog(Nf,EN)
    plt.loglog(Nf,EP)
    plt.loglog(Nf,EE)
    plt.grid(True,which="both",ls="--")
    plt.title("log-log Strain Amplitude vs Cycles to Failure",fontdict=font)
    plt.ylabel("Strain Amplitude (m/m)",fontdict=font)
    plt.xlabel("Cycles to Failure (N)",fontdict=font)
    plt.legend(["Total Strain-Life","Plastic Strain-Life","Elastic Strain-Life"],loc = 1)
    plt.ylim([EN[-1],EN[0]])
    plt.xlim([1,len(Nf)])
    plt.savefig(png_dir + '/Total_StrainLife.png',bbox_inches='tight')
    plt.savefig(pdf_dir + '/Total_StrainLife.pdf',bbox_inches='tight')
#    
    #PLot Plastic Strain-life
    plt.figure()
    plt.plot(Rf,EP,'r--')
    plt.scatter(Rev_F,E_AmpP,color='black')
    for i in range(len(Rev_F)):
        if Rev_F[i] == 4000000:
            plt.scatter(Rev_F[i],E_AmpP[i],color = 'red')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True,which="both",ls="--")
    plt.xlabel("Reversals to Failure",fontdict=font)
    plt.ylabel("Plastic Strain Amplitude",fontdict=font)
    plt.title("Plastic Strain-Life",fontdict = font)
    plt.savefig(png_dir + '/Plastic_StrainLife.png',bbox_inches='tight')
    plt.savefig(pdf_dir + '/Plastic_StrainLife.pdf',bbox_inches='tight')
#    
    #Plot Elastic Strain-Life
    plt.figure()
    plt.plot(Rf,EE*E,'r--')
    plt.scatter(Rev_F,S_Amp,color='black')
    for i in range(len(Rev_F)):
        if Rev_F[i] == 4000000:
            plt.scatter(Rev_F[i],S_Amp[i],color = 'red')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True,which="both",ls="--")
    plt.xlabel("Reversals to Failure",fontdict=font)
    plt.ylabel("True Stress Amplitude",fontdict=font)
    plt.title("Elastic Strain-Life",fontdict = font)
    plt.savefig(png_dir + '/Elastic_StrainLife.png',bbox_inches='tight')
    plt.savefig(pdf_dir + '/Elastic_StrainLife.pdf',bbox_inches='tight')
#    
    #Plot Cyclic Stress-Strain Curve
    plt.figure()
    plt.scatter(E_Amp,S_Amp*10**-6,color='black')
    plt.plot(cycE_Amp,cycS_Amp*10**-6,'r--')
    plt.grid(True)
    plt.ylim([0,(max(S_Amp*10**-6) + 1)])
    plt.xlim([0,(max(E_Amp)+0.01)])
    plt.title("Cyclic Stress-Strain Curve",fontdict=font)
    plt.xlabel("Cyclic Strain (m/m)",fontdict=font)
    plt.ylabel("Cyclic Stress (MPa)",fontdict=font)
    plt.legend(["Cyclic S-E","Hysteresis Loop Tips"])
    plt.savefig(png_dir + '/Cyclic_StressStrain.png',bbox_inches='tight')
    plt.savefig(pdf_dir + '/Cyclic_StressStrain.pdf',bbox_inches='tight')
#    
#    
    #Plot Stress-Life
    plt.figure()
    plt.plot(Nf,SN*10**-6,'r--')
    plt.scatter(Cycf,S_Rng*10**-6,color='black')
    for i in range(len(Cycf)):
        if Cycf[i] == 2000000:
            plt.scatter(Cycf[i],S_Rng[i]*10**-6,color = 'red')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True,which="both",ls="--")
    plt.xlabel("Cycles to Failure",fontdict=font)
    plt.ylabel("Stress Range (MPa)",fontdict=font)
    plt.title("Stress Range vs. Cycles to Failure",fontdict=font)
    plt.savefig(png_dir + '/StressLife.png',bbox_inches='tight')
    plt.savefig(pdf_dir + '/StressLife.pdf',bbox_inches='tight')
    #
    print("Finished.")
    print("************************************")
#==============================================================================
#==============================================================================
# K. Gahan, 2019
