from pint import UnitRegistry, set_application_registry
import pint.formatting
import os

from .checks import *
from .conversions import *

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


# concise function for printing quantities (i.e. numbers with units) with
# formatting for the units
def pq(q, precision=3, scientific=False):
    if scientific:
        num_type = 'g'
    else:
        num_type = 'f'
    print("{:0.{}{}~M}".format(q, precision, num_type))
