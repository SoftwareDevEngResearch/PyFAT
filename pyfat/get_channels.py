import pandas as pd

def mono_channels(file):
    """Defines the column name for each monotonic data channel based on the 
    channel headers. 
    Defines stress and geometry columns separately from others b/c
    some data will have stress, some will not. Same with geometry"""

    #Read data file...
    data = pd.read_csv(file,header=0)

    #Get file headers as a list...
    channel_names = data.columns
    
    #Change headers to standard format for identification...
    std_names = []
    for channel_name in channel_names:
        channel_name = str(channel_name).replace(" ","").lower()
        std_names.append(channel_name)

    #Loop for defining main channels...
    i = 0
    stress_bool = False
    width_bool = False
    thick_bool = False
    geo_bool = False

    for name in std_names:

        #Use logic to identify consistent channels...
        if "position" in name:
            pos_col = channel_names[i]
        elif "load" in name:
            load_col = channel_names[i]
        elif "axialstrain" in name:
            ax_col = channel_names[i]
        elif "transversestrain" in name:
            tr_col = channel_names[i]

        #Use boolean to identify inconsistent channels...
        elif "stress" in name:
            stress_bool = True
            stress_col = channel_names[i]
        elif "width" in name:
            width_bool = True
            width_col = channel_names[i]
        elif "thickness" in name:
            thick_bool = True
            thick_col = channel_names[i]
        i += 1

    channels = [
        pos_col, load_col, ax_col, tr_col
    ]

    #Append stress or geometry...
    geo_bool = False
    if stress_bool:
        channels.append(stress_col)
    elif width_bool and thick_bool:
        channels.append(width_col)
        channels.append(thick_col)
        geo_bool = True
    elif stress_bool and width_bool and thick_bool:
        raise AttributeError(
            "Data must contain stress OR sample geometry, not both"
        )
    else:
        raise AttributeError(
            "Data must contain stress OR sample width AND thickness"
        )

    return channels, stress_bool, geo_bool


def fatigue_channels(file):
    """Defines the column name for each fatigue data channel based on the 
    channel headers. 
    Defines stress and geometry columns separately from others b/c
    some data will have stress, some will not. Same with geometry"""

    #Read data file...
    data = pd.read_csv(file,header=0)

    #Get file headers as a list...
    channel_names = data.columns
    
    #Change headers to standard format for identification...
    std_names = []
    reg_names = []
    for channel_name in channel_names:
        reg_names.append(channel_name)
        channel_name = str(channel_name).replace(" ","").lower()
        std_names.append(channel_name)
    
    #Loop for defining main channels...
    i = 0
    stress_bool = False
    width_bool = False
    thick_bool = False
    geo_bool = False

    for name in std_names:

        if "cycle" in name and not "time" in name:
            cycles_col = reg_names[i]
        elif "max" in name and "load" in name:
            max_load_col = reg_names[i]
        elif "min" in name and "load" in name:
            min_load_col = reg_names[i]
        elif "axialstrain" in name and "max" in name:
            max_str_col = reg_names[i]
        elif "axialstrain" in name and "min" in name:
            min_str_col = reg_names[i]
        
        #Use boolean to identify inconsistent channels...
        elif "stress" in name and "max" in name:
            stress_bool = True
            max_stress_col = reg_names[i]
        elif "stress" in name and "min" in name:
            stress_bool = True
            min_stress_col = reg_names[i]
        elif "width" in name:
            width_bool = True
            width_col = reg_names[i]
        elif "thickness" in name:
            thick_bool = True
            thick_col = reg_names[i]

        i += 1

    channels = [
        cycles_col, max_load_col, min_load_col, max_str_col, min_str_col
    ]

    #Append stress or geometry...
    geo_bool = False
    if stress_bool:
        channels.append(max_stress_col)
        channels.append(min_stress_col)
    elif width_bool and thick_bool:
        channels.append(width_col)
        channels.append(thick_col)
        geo_bool = True
    elif stress_bool and width_bool and thick_bool:
        raise AttributeError(
            "Data must contain stress OR sample geometry, not both"
        )
    else:
        raise AttributeError(
            "Data must contain stress OR sample width AND thickness"
        )

    return channels, stress_bool, geo_bool




