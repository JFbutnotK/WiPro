import numpy as np
import schrodinger.schrodinger_solve as solve

def energy(lvl, res, mass):
    return (lvl + 1) ** 2 * np.pi ** 2 / mass / res ** 2 / 2.0

def test_infinite():
    raw_data = solve.import_input("test/infinitePot")
    data_dict = solve.save_variables(raw_data)
    solve.abkurzung(data_dict)
    solve.interpolation(data_dict)
    solve.schrodinger_eq(data_dict)
    solve.expval(data_dict)
    res = np.abs(data_dict['gitter'][0]-data_dict['gitter'][-1])
    nrg_theo = np.zeros(len(data_dict['eigval']))
    

    for lvl in range(len(data_dict['eigval'])):
        nrg_theo[lvl] = energy(lvl, res, data_dict['m'])
        

    assert np.allclose(data_dict['eigval'], nrg_theo, rtol=1e-2)
