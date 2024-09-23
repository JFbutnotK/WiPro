import pytest
import sys
import numpy as np
from pathlib import Path
import schrodinger.schrodinger_solve as solve
sys.path.insert(0, str(Path.cwd().parent))


TESTS = ['finitePot', 'asymPot', 'doublePotCSpline', 'doublePotLinear', 'harmOsc', 'infinitePot']
DATA_DICT={}






@pytest.mark.parametrize('test', TESTS)
def test_potential(test: str):
    potential_old = np.loadtxt(f'test/{test}/potential.dat')[:, 1]
    potential_new = DATA_DICT[test]['potenzial']
    assert np.allclose(potential_new, potential_old, rtol=1e-10)

@pytest.mark.parametrize('test', TESTS)
def test_eigvec(test: str):
    potential_old = np.loadtxt(f'test/{test}/wavefuncs.dat')[:, 1:]
    potential_new = DATA_DICT[test]['eigvec']
    assert np.allclose(potential_new, potential_old, rtol=1e-10)


def setup_module():
    for test in TESTS:
        raw_data = solve.import_input(f"test/{test}")
        data_dict = solve.save_variables(raw_data)
        solve.abkurzung(data_dict)
        solve.interpolation(data_dict)
        solve.schrodinger_eq(data_dict)
        solve.expval(data_dict)
        DATA_DICT[test] = data_dict

def main():
    setup_module()
    print(DATA_DICT)

if __name__ == '__main__':
    main()