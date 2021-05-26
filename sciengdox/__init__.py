from . import compiledoc
from . import constants
from . import figures
from . import tables
from . import units


# concise function for printing and including computed markdown.  The pandoc
# filter looks for this function and handles it specially.
def pmd(markdown):
    print(markdown)


# concise functions for printing floats and integers.  The pandoc filter looks
# for these functions and handles them specially.
def pf(f, precision=3, scientific=False):
    units.pq(f, precision, scientific)


def pi(i):
    units.pq(i, 0, False)
