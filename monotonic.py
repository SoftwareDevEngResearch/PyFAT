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
        self.channels = channels
        self.stress_bool = stress_bool
        self.geo_bool = geo_bool
 
    
    def get_stress(self,channels,stress_bool,geo_bool):
        if stress_bool:
            stress = channels[4]


