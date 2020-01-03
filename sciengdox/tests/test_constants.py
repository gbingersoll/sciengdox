from pytest import approx
from sciengdox.units import ureg
import sciengdox.constants as constants


def test_c0_has_correct_units_and_value():
    assert constants.c0.m == approx(299792458)
    assert constants.c0.u == ureg.parse_units('m / s')


def test_planck_constant_has_correct_units_and_value():
    assert constants.h.m == approx(6.62607004e-34, abs=1e-40)
    assert constants.h.u == ureg.parse_units('m^2 kg / s')


def test_proton_mass_has_correct_units_and_value():
    assert constants.proton_mass.m == approx(1.6726219e-27, abs=1e-34)
    assert constants.proton_mass.u == ureg.parse_units('kg')


def test_g_has_correct_units_and_value():
    assert constants.g.m == approx(9.80665, abs=1e-6)
    assert constants.g.u == ureg.parse_units('m/s^2')
