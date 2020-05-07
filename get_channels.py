import pandas as pd

class Channels:

    def __init__(self,file):

        def get_channels(data):
            """Defines the column name for each data channel based on the 
            channel headers. 
            Defines stress and geometry columns separately from others b/c
            some data will have stress, some will not. Same with geometry"""

            #Get file headers as a list...
            channel_names = list(data[:0])
            
            #Change headers to standard format for identification...
            short_names = []
            for channel_name in channel_names:
                channel_name = str(channel_name)
                channel_name.replace(" ","").lower()
                short_names.append(channel_name)
            print("TEST: ",short_names)

            #Loop for defining main channels...
            for name in channel_names:

                #Use logic to identify main channels...
                if "position" in name:
                    pos_col = name
                elif "load" in name:
                    load_col = name
                elif "axialstrain" in name:
                    ax_col = name
                elif "transversestrain" in name:
                    tr_col = name  
                elif "stress" in name:
                    stress_col = name

            #Define dynamic channels (stress, geometry)...
            #    

            main_channels = [
                pos_col, load_col, ax_col, tr_col
            ]
                
            return main_channels

        self.data = pd.read_csv(file,header=0)
        self.main_channels = get_channels(self.data)

        