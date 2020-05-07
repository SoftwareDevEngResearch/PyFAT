#------------------------------#
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from pathlib import Path

import get_channels
#------------------------------#
#
class Monotonic:
    """Takes in monotonic (tensile test) data and performs necessary processing
    """
    def __init__(self, channels, file):
        """Initializes the analysis for a single file with data channels defined
        """
        self.data = pd.read_csv(file,header=0)
        self.channels = channels

        #self.time = self.data[self.channels[0]]
 
    
    def get_stress(self):
        pass
        w = 13 #mm width
        t = 5 #mm thickness
        if self.channels[3] == "":
            stress = self.load/(w*t)
        else:
            stress = self.stress

        




if __name__ == "__main__":
    workingfile = Path(
            os.path.dirname(os.path.realpath(__file__)),"Data_Files","M-4-D.csv"
        )
    workingchannels = get_channels.Channels(workingfile).channels
    
    test1 = Monotonic(workingchannels,workingfile)

    #stress = test1.get_stress()
    #print(stress)