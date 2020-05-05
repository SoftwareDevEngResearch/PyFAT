
    #################################################
    #   Python FATigue Test Data Analysis Package   #
    #                  Version 1.0                  #
    #                                               #
    #                  Kevan Gahan                  #
    #################################################

#-----------------------#
from pathlib import Path
import subprocess
import os

import monotonic
import get_channels
#-----------------------#


def iterate(choice,path):
    """performs iteration of analysis. Takes in user input for analysis 
    type and directory path to data, performs analysis iteration for 
    selected analysis type"""

    #Get list of files in directory
    files = next(os.walk(path))[2]
    #Remove hidden folders/files from list
    for file in files:
        if file[0] == ".":
            files.remove(file)

    #Get channel names from first file 
    file_channels = get_channels.Channels(Path(path,files[0]))
            
    print("Beginning Analysis Iteration...")
    for file in files:
        this_file = Path(path,file)
        name = str(file)
        print("    Reading File ",name)
                                                                            
        #Start the Analysis
        if choice == "m":
            monotonic.Monotonic(file_channels, this_file)
        elif choice =="f":
            pass


def get_monotonic_path():
    """Asks user to input the directory path to folder containing 
    monotonic data. Incorporates bash to auto-complete path entries"""
    print(
        "*****************************************************\n"
        "Monotnic Analysis Selected..."    
    )
    path=subprocess.check_output(
        'read -e -p "Enter Directory Containing '
        'Monotonic Data:" var ; echo $var',shell=True
    ).rstrip()
    return path
   

def get_fatigue_path():
    """Asks user to input the directory path to folder containing 
    fatigue data. Incorporates bash to auto-complete path entries"""

    print("*****************************************************\n"
        "Fatigue Analysis Selected..."
        
    )
    path=subprocess.check_output(
        'read -e -p "Enter Directory Containing Fatigue Data:" var ; echo $var',shell=True
    ).rstrip()
    return path


def welcome():
    """Welcomes user to the program, asks for analysis type.
    Returns chosen string analysis type and string directory path"""

    print(
        "*****************************************************\n"
        "Welcome to PyFAT - Python Material Test Data Analysis\n"
        "                      Version 1.0                    \n"
        "*****************************************************\n"  
        "Would you like to analyze Monotonic or Fatigue Data?"  
    )
    choice = input("Type \"m\" for Monotonic or \"f\" for Fatigue: ")
    if choice == "m":
        path = get_monotonic_path()
    elif choice =="f":
        path = get_fatigue_path()
    return choice, path



if __name__ == "__main__":
    choice, path = welcome()
    path = str(path.decode('utf-8'))
    print(path)
    iterate(choice,path)



