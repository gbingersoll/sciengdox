from pytest import raises
from sciengdox.units import Q_
from sciengdox.units.checks import (
    check_dims,
    NoDimensionsError,
    WrongDimensionalityError,
)


def test_check_dims_passes_if_units_match_exactly():
    check_dims(Q_(7, "kg"), "kg")
    pass


def test_check_dims_passes_if_units_match_type():
    check_dims(Q_(7, "m"), "[length]")
    pass


def test_check_dims_passes_if_supposed_to_be_unitless():
    check_dims(Q_(7, ""), "")
    pass


def test_check_dims_passes_if_supposed_to_be_unitless_and_just_a_number():
    check_dims(13.1, "")
    pass


def test_check_dims_raises_if_quantity_is_just_a_number():
    with raises(NoDimensionsError) as excinfo:
        check_dims(7, "kg")
    assert (
        str(excinfo.value)
        == "Parameter is dimensionless.  Needs to have dimensions of 'kg'."
    )


def test_check_dims_raises_if_quantity_has_wrong_dimensionality():
    with raises(WrongDimensionalityError) as excinfo:
        check_dims(Q_(1, "m"), "s")
    assert (
        str(excinfo.value) == "Parameter needs to have dimensions of 's',"
        " has dimensions of '[length]'."
    )
    with raises(WrongDimensionalityError) as excinfo:
        check_dims(Q_(1, "kg"), "[time]")
    assert (
        str(excinfo.value) == "Parameter needs to have dimensions of '[time]',"
        " has dimensions of '[mass]'."
    )


def test_check_dims_raises_if_quantity_should_be_dimensionless():
    with raises(WrongDimensionalityError) as excinfo:
        check_dims(Q_(1, "m"), "")
    assert (
        str(excinfo.value) == "Parameter needs to be dimensionless,"
        " has dimensions of '[length]'."
    )
