import os, sys, numpy as np, pytest, pandas as pd
from pathlib import Path


main_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(main_dir,'..'))

import fatigue


#Test File: 9-4.csv

@pytest.fixture
def test_run():
    cwd = os.path.dirname(os.path.abspath(__file__))
    file1 = Path(cwd,"inputs","fatigue_data_ex1.csv")

    channels = [
        "Elapsed Cycles", "Load(8800 (0,1):Load):Maximum (kN)", 
        "Load(8800 (0,1):Load):Minimum (kN)", 
        "Strain(8800 (0,1):Axial Strain):Maximum (%)",
        "Strain(8800 (0,1):Axial Strain):Minimum (%)", "width", "thickness"
    ]

    run = fatigue.Fatigue(channels, False, True, 1902, file1)

    return run

def test_get_HLC(test_run):

    test_index = test_run.HLC
    exp_index = 5329

    assert test_index == exp_index

def test_get_true_stress(test_run):

    test_max, test_min = test_run.get_true_stress()

    assert np.allclose(test_max,19231031,1)
    assert np.allclose(test_min,-26151965,1)

def test_get_true_strain(test_run):
    
    test_max, test_min = test_run.get_true_strain()

    assert np.allclose(test_max, 0.0112621, 1e-4)
    assert np.allclose(test_min, -0.0112919, 1e-4)

def test_calc_strains(test_run):

    max_stress, min_stress = test_run.get_true_stress()
    max_strain, min_strain = test_run.get_true_strain()
    
    test_max_pl, test_min_pl, test_max_el, test_min_el = test_run.calc_strains(
        max_stress, min_stress, max_strain, min_strain
    )

    assert np.allclose(test_max_pl, 0.00115117715941, 1e-3)
    assert np.allclose(test_min_pl, 0.00245781377480, 1e-3)
    assert np.allclose(test_max_el, 0.01011095238475, 1e-3)
    assert np.allclose(test_min_el, -0.01374971919834, 1e-3)


def test_data_fit():
    
    cwd = os.path.dirname(os.path.abspath(__file__))
    HL_file = Path(cwd,"inputs","HL_Data_ex.csv",header=1)

    data = pd.read_csv(HL_file)

    test_coeff, test_exp, test_SE = fatigue.data_fit(
        data['StressAmp'], data['MaxCycles']
    )

    test_coeff = round((test_coeff*10**-6),4)
    test_exp = round(test_exp,5)
    test_SE = round(test_SE,4)

    assert np.allclose(test_coeff, 845, 1)
    assert np.allclose(test_exp,-0.4261, 1e-2)
    assert np.allclose(test_SE, 0.4286, 1e-2)
    
    


