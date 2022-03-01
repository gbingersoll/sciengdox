from pint import UnitRegistry, set_application_registry
from pint.formatting import formatter, register_unit_format
import os

from .checks import *  # noqa: F401, F403
from .conversions import *  # noqa: F401, F403

ureg = UnitRegistry()
try:
    ureg.setup_matplotlib()
except ModuleNotFoundError:
    pass
set_application_registry(ureg)
Q_ = ureg.Quantity

# Loading local definitions
def_file = f"{os.path.dirname(os.path.realpath(__file__))}/unit_defs.txt"
ureg.load_definitions(def_file)


# Add Markdown format for Quantities
@register_unit_format("M")
def format_markdown(unit, registry, **options):
    return formatter(
        unit.items(),
        as_ratio=True,
        single_denominator=True,
        product_fmt=r" ",
        division_fmt=r"{}/{}",
        power_fmt=r"{}^{}^",
        parentheses_fmt=r"({})",
        **options,
    )


# concise function for printing quantities (i.e. numbers with units) with
# formatting for the units
def pq(q, precision=3, scientific=False):
    try:
        q.units
    except AttributeError:
        q = Q_(q, "")

    if scientific:
        num_type = "g"
    else:
        num_type = "f"
    print("{:0.{}{}~M}".format(q, precision, num_type))
