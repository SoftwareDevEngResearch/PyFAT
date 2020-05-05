import pandas as pd

class Channels:
    def __init__(self,file):

        def get_channels(data):
            """Defines the column #'s for each data channel
            Note: This really only needs to happen once, not for every file 
            (b/c they will all be formatted the same). Update that later to 
            only happen for the 1st file"""
            #Get headers as a list...
            channel_names = list(data[:0])          
            #Define the channels needed for analysis...
            for i in range(len(channel_names)):
                name = channel_names[i]
                if "Total Time" in name:
                    time_col = name
                elif "Position" in name:
                    pos_col = name
                elif "Load" in name:
                    load_col = name
                elif "Stress" in name:
                    stress_col = name
                elif "Axial Strain" in name:
                    ax_col = name
                elif "Transverse Strain" in name:
                    tr_col = name
                else:
                    #some data will have a stress channel, some will not...
                    stress_col = "" 
            channels = [
                time_col, pos_col, load_col, stress_col, ax_col, tr_col
            ]
            print(channels)
            return channels

        self.data = pd.read_csv(file,header=0)
        self.channels = get_channels(self.data)

        