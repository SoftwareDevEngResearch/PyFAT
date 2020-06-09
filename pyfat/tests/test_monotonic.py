import os, sys, numpy as np, pytest
from pathlib import Path


main_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(main_dir,'..'))

import monotonic

@pytest.fixture
def test_run():
    cwd = os.path.dirname(os.path.abspath(__file__))
    file1 = Path(cwd,"inputs","mono_data_ex1.csv")

    channels1 = [
            "Position(8800 (0,1):Position) (mm)", "Load(8800 (0,1):Load) (kN)",
            "Strain(8800 (0,1):Axial Strain) (%)", 
            "Strain(8800 (0,1):Transverse Strain) (%)", "width", "thickness"
        ]

    run = monotonic.Monotonic(channels1, False, True, file1)

    return run


def test_get_positions(test_run):

    p1, p2, ext = test_run.get_positions()

    assert np.allclose(p1, 0.0456697, 1e-4)
    assert np.allclose(p2, 0.05646, 1e-4)
    assert np.allclose(ext, 0.010794, 1e-4)


def test_get_true(test_run):

    true_stress, true_strain = test_run.get_true()

    test_true_stress = test_run.stress*(1 + test_run.ax_str)
    test_true_strain = np.log(test_run.ax_str + 1)

    assert np.allclose(true_stress, test_true_stress)
    assert np.allclose(true_strain,test_true_strain)


def test_get_modulus_and_poissons(test_run):

    test_ratio, test_emod = test_run.get_modulus_and_poissons()

    assert np.allclose(test_emod,1989259156,1)
    assert np.allclose(test_ratio,0.401669,1e-4)

def test_get_offset(test_run):

    test_ratio, test_emod = test_run.get_modulus_and_poissons()

    test_offset_strain, test_offset_stress = test_run.get_offset(test_emod)

    assert np.allclose(test_offset_stress,30851054.65,1)
    assert np.allclose(test_offset_strain,0.017555693, 1e-4) 

def test_get_yield(test_run):

    test_yield_stress, test_yield_strain, test_max_load = test_run.get_yield()

    exp_yield_stress = max(test_run.stress)

    assert np.allclose(test_yield_stress,exp_yield_stress,1)
    assert np.allclose(test_yield_strain, 0.05186841, 1e-4)
    assert np.allclose(test_max_load,3190,1)

def test_get_engr_fracture(test_run):

    test_frac_strength, test_max_ax, test_max_tr = test_run.get_engr_fracture()

    assert np.allclose(test_frac_strength, 41546772, 1)
    assert np.allclose(test_max_ax, 0.117463352, 1e-4)
    assert np.allclose(test_max_tr, 0.061092187, 1e-4)





