from pint import UnitRegistry, set_application_registry
import pint.formatting
import os

from .checks import *
from .conversions import *

ureg = UnitRegistry()
ureg.setup_matplotlib()
set_application_registry(ureg)
Q_ = ureg.Quantity

# Loading local definitions
def_file = f"{os.path.dirname(os.path.realpath(__file__))}/unit_defs.txt"
ureg.load_definitions(def_file)

# Add Markdown format for Quantities
pint.formatting._FORMATS['M'] = {
    'as_ratio': True,
    'single_denominator': True,
    'product_fmt': r' ',
    'division_fmt': r'{}/{}',
    'power_fmt': '{}^{}^',
    'parentheses_fmt': r'({})',
}
pint.formatting._KNOWN_TYPES = \
    frozenset(list(pint.formatting._FORMATS.keys()) + ['~'])
