import pandas as pd

class Channels:

    def __init__(self,file):

        def get_channels(data):
            """Defines the column #'s for each data channel based on the 
            channel headers. 
            Note: this needs to be made more universal"""

            #Get file headers as a list...
            channel_names = list(data[:0])    

            for channel_name in channel_names:
                #Change headers to standard format for identification...
                name = channel_name.replace(" ","").lower()
                #Use logic to identify channels...
                if "position" in name:
                    pos_col = name
                elif "load" in name:
                    load_col = name
                elif "axialstrain" in name:
                    ax_col = name
                elif "transversestrain" in name:
                    tr_col = name
                #Some data will have a stress column, some will not...
                if "stress" in name:
                    stress_col = name
                    width_col = ""
                    thick_col = ""
                elif "width" in name:
                    stress_col = ""
                    width_col = name
                elif "thickness" in name:
                    stress_col = ""
                    thick_col = name
                else:
                    raise ValueError(
                        "Data must contain stress or width & thickness columns"
                    )

            channels = [pos_col, load_col, ax_col, tr_col]

            #Append stress or cross-section information...
            if stress_col=="":
                channels.append(width_col)
                channels.append(thick_col)
                
            elif width_col=="":
                channels.append(stress_col)
                
            return channels

        self.data = pd.read_csv(file,header=0)
        self.channels = get_channels(self.data)

        