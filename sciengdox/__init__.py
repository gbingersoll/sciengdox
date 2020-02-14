from . import constants
from . import figures
from . import tables
from . import units


# concise function for printing and including computed markdown.  The pandoc
# filter looks for this function and handles it specially.
def pmd(markdown):
    print(markdown)
