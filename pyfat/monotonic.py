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
    def __init__(self, channels, stress_bool, geo_bool, file):
        """Initializes the analysis for a single file with data channels defined
        """
        self.data = pd.read_csv(file,header=0)
        self.position = self.data[channels[0]]
        self.load = self.data[channels[1]]
        self.ax_str = self.data[channels[2]]
        self.tr_str = self.data[channels[3]]

        if stress_bool:
            self.stress = self.data[channels[4]]
        elif geo_bool:
            self.width = self.data[channels[4]][0]
            self.thickness = self.data[channels[5]][0]
            #self.stress = self.load/(self.width*self.thickness)
        #print(self.stress)

    """
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
    #stress = get_stress(stress_bool,geo_bool)
    #print("STRESS=",stress)

        


