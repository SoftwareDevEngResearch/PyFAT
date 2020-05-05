#------------------------------#
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from pathlib import Path

import monotonic_functions
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

        self.time = self.data[self.channels[0]]
        self.position = self.data[self.channels[1]]
        self.load = self.data[self.channels[2]]
        self.axial_strain = self.data[self.channels[4]]
        self.trans_strain = self.data[self.channels[5]]
        if self.channels[3] == "":
            pass
        else:
            self.stress = self.data[self.channels[3]]
    
    def get_stress(self):
        pass
        w = 13 #mm width
        t = 5 #mm thickness
        if self.channels[3] == "":
            stress = self.load/(w*t)
        else:
            stress = self.stress

        




if __name__ == "__main__":
    test1 = Monotonic(
        Path(
            os.path.dirname(os.path.realpath(__file__)),"Data_Files","M-4-D.csv"
        )
    )
    stress = test1.get_stress()
    print(stress)