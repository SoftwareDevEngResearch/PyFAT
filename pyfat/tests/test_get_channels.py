import os, sys
from pathlib import Path

main_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(main_dir,'..'))

import get_channels


def test_mono_channels():

    """Test for correct channel header identification and stress/geometry bools
    for MONOTONIC data for two data file types"""

    cwd = os.path.dirname(os.path.abspath(__file__))
    file1 = Path(cwd,"inputs","mono_data_ex1.csv")
    file2 = Path(cwd,"inputs","mono_data_ex2.csv")

    channels1, stressb1, geob1 = get_channels.mono_channels(
        file1
    )

    channels2, stressb2, geob2 = get_channels.mono_channels(
        file2
    )

    assert channels1 == [
        "Position(8800 (0,1):Position) (mm)", "Load(8800 (0,1):Load) (kN)",
        "Strain(8800 (0,1):Axial Strain) (%)", 
        "Strain(8800 (0,1):Transverse Strain) (%)", "width", "thickness"
    ]

    assert geob1 == True
    assert stressb1 == False

    assert channels2 == [
        ' "Position (mm)"', ' "Load (N)"', ' "AxialStrain (mm/mm)"',
        ' "TransverseStrain (mm/mm)"', ' "Stress (MPa)"'
    ]

    assert geob2 == False
    assert stressb2 == True



def test_fatigue_channels():

    """Test for correct channel header identification and stress/geometry bools
    for FATIGUE data for two data file types"""

    cwd = os.path.dirname(os.path.abspath(__file__))
    file1 = Path(cwd,"inputs","fatigue_data_ex1.csv")
    file2 = Path(cwd,"inputs","fatigue_data_ex2.csv")

    channels1, stressb1, geob1 = get_channels.fatigue_channels(
        file1
    )

    channels2, stressb2, geob2 = get_channels.fatigue_channels(
        file2
    )

    assert channels1 == [
        "Elapsed Cycles", "Load(8800 (0,1):Load):Maximum (kN)", 
        "Load(8800 (0,1):Load):Minimum (kN)", 
        "Strain(8800 (0,1):Axial Strain):Maximum (%)",
        "Strain(8800 (0,1):Axial Strain):Minimum (%)", "width", "thickness"
    ]

    assert geob1 == True
    assert stressb1 == False

    assert channels2 == [
        'Cycle', ' "Max Load (N)"', ' "Min Load (N)"',' "Max AxialStrain (mm)"',
        ' "Min AxialStrain (mm)"', ' "Max Stress (MPa)"', ' "Min Stress (MPa)"'
    ]

    assert geob2 == False
    assert stressb2 == True