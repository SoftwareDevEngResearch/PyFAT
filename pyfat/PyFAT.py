
    #################################################
    #   Python FATigue Test Data Analysis Package   #
    #                  Version 1.0                  #
    #                                               #
    #                  Kevan Gahan                  #
    #################################################

#-----------------------#
from pathlib import Path
import os
import argparse
#--------#
import monotonic
import get_channels
#-----------------------#


def io_sorter(input_file):
    """Reads the input file for the data input location and the 
    output location (where to save results to)."""

    with open(Path(input_file),'r') as input_file:
        lines = input_file.readlines()

    for line in lines:
        #Remove and spaces...
        std_line = line.replace(" ","")
        #Assign file paths...
        if std_line.startswith("INPUT="):
            input_loc = std_line[6:]
        elif std_line.startswith("OUTPUT="):
            output_loc = std_line[7:]
        elif std_line.startswith("#") or std_line.startswith(""):
            pass
        else:
            raise AttributeError(
                "Input file is not formatted correctly. Refer to Documentation."
            )

    return input_loc, output_loc


def analysis(input_path, output_path, monotonic_bool, fatigue_bool):
    """performs iteration of analysis. Takes in user input for analysis 
    type and directory path to data, performs analysis iteration for 
    selected analysis type. Saves results to user-defined save location."""

    #Get list of data files in input directory
    input_dir = str(input_path).strip()
    output_dir = str(output_path).strip()
    files = next(os.walk(input_dir))[2]
    
    #Remove hidden folders/files from list
    for filename in files:
        if filename.startswith("."):
            files.remove(filename)
    
    #Get channel names from first file 
    if monotonic_bool:
        channels, stress_bool, geo_bool = get_channels.mono_channels(
            Path(input_dir,files[0])
        )
    elif fatigue_bool:
        channels, stress_bool, geo_bool = get_channels.fatigue_channels(
            Path(input_dir, files[0])
        )

    #Start the Analysis...        
    if monotonic_bool:
        print("==================== MONOTONIC ANALYSIS ===================")
        monotonic.mono_analysis(
            input_dir, output_dir, files, channels, stress_bool, geo_bool
        )
        
    elif fatigue_bool:
        pass #Pass for now ----- NEED TO ADD FATIGUE FUNCTIONALITY LATER
    """
        fatigue.fatigue_analysis(
            input_dir, files, channels, stress_bool, geo_bool
        )
    """


def main():
    """Parses command-line inputs. Reads in the input file, determines
    input file contents (i/o locations), calls on analysis iteration"""

    #Add command-line inputs ...
    parser = argparse.ArgumentParser(
        description='Process monotonic or fatigue material test data'
    )

    parser.add_argument(
        "input",help="The path to the input file",type = str
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-m','--monotonic',help="Perform analysis for monotonic data",
        action="store_true"
        )
    group.add_argument(
        '-f','--fatigue',help='Perform analysis for fatigue data',
        action="store_true"
    )

    parser.add_argument(
        '-e','--elasticmodulus',help='Elastic modulus value given in MPa'
    )

    args = parser.parse_args()

    #Get args...
    input_file = args.input
    monotonic_bool = args.monotonic
    fatigue_bool = args.fatigue
    modulus = args.elasticmodulus

    #Read input file...
    input_path, output_path = io_sorter(input_file)

    #Begin selected analysis type...
    analysis(
        input_path, output_path, monotonic_bool, fatigue_bool
    )
  

if __name__ == "__main__":

    #Print welcome message...
    print(
        "***********************************************************\n"
        "*  Welcome to PyFAT - Python Material Test Data Analysis  *\n"
        "*                       Version 1.0                       *\n"
        "***********************************************************\n"
    )

    main()
    



