class NoDimensionsError(Exception):
    def __init__(self, exp_dims):
        Exception.__init__(
            self,
            "Parameter is dimensionless.  "
            f"Needs to have dimensions of '{exp_dims}'.",
        )


class WrongDimensionalityError(Exception):
    def __init__(self, exp_dims, act_dims):
        exp_msg = f"have dimensions of '{exp_dims}'"
        if exp_dims == "":
            exp_msg = "be dimensionless"

        Exception.__init__(
            self, f"Parameter needs to {exp_msg}, has dimensions of '{act_dims}'."
        )


def check_dims(param, expected_dims):
    try:
        if not param.check(expected_dims):
            raise WrongDimensionalityError(expected_dims, param.dimensionality)
    except AttributeError:
        if expected_dims != "":
            raise NoDimensionsError(expected_dims)
