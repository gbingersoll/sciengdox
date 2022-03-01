from pytest import approx
from sciengdox.units.conversions import mag2db, db2mag, pwr2db, db2pwr


def test_mag2db_converts_from_magnitude_to_dB():
    assert mag2db(0.7) == approx(-3.098039)
    assert mag2db(10.2) == approx(20.172003)


def test_db2mag_converts_from_dB_to_magnitude():
    assert db2mag(-2) == approx(0.794328)
    assert db2mag(5) == approx(1.778279)


def test_pwr2db_converts_from_power_to_dB():
    assert pwr2db(0.6) == approx(-2.218487496)
    assert pwr2db(2.3) == approx(3.61727836)


def test_db2pwr_converts_from_dB_to_power():
    assert db2pwr(-4.2) == approx(0.380189396)
    assert db2pwr(7.3) == approx(5.370317964)
