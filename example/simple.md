---
title: Example Document
author: [Author]
...

# Code Listings

```{#lst:simple_listing2 .ruby caption="Listing of Ruby code"}
# A simple class
class Hello
  def go
    puts "Hello World"
  end
end
```

```{#lst:simple_listing3 .python .noexec caption="Listing of Python code that is just printed"}
# A simple class
class Hello:
    def go(__self__):
        print("Hello World")
```

# Code Execution

Defining this code block will echo the code block itself to the document and
also will execute it, printing the output to the document as well.

```{.python .echo}
class Greeter:
    def speak(__self__):
        print("Hello World")

    def respond(__self__, name, polite=False):
        if polite:
            print(f"Hello {name}.  How are you?")
        else:
            print(f"Hello {name}")

greeter = Greeter()
greeter.speak()
```

This next code block continues from the previous one, so variables stay defined.

```{.python .echo}
greeter.respond("Joe")
greeter.respond("Joe", polite=True)
```

```{.python}
my_value = 37
```

The block right above this one in the markdown is not printed, but it
establishes the value `my_value`{.python}.  This defaults to printing as plain
text to match the surrounding paragraph, but you can also keep a result
formatted as monospace code by including `.asCode` in its classes like this:
`2*my_value`{.python .asCode}.  You can also wrap the result in an equation like
$3x=`3*my_value`{.python}$.  This works for equation blocks too as in
@eq:equation-with-code-eval.

$$
y = -5x + 0.5 = `-5 * my_value + 0.5`{.python}
$$ {#eq:equation-with-code-eval}


# Figures

We can use Markdown for figures with captions and so on.

```{.python .echo}
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sciengdox
from sciengdox.figures import svg_figure

t = np.linspace(0, 5, 300)
num_sines = 2
f = 3*np.sin(2 * np.pi * 2 * t) + 1.8*np.cos(2 * np.pi * 0.2 * t)
fig, ax = plt.subplots(1, 1)
crv, = ax.plot(t, f)
```

![Sum of `num_sines`{.python} sines](`svg_figure(fig, 'sines')`{.python}){#fig:sines width=50%}

Later, we can reference these figures. For instance, @fig:sines is an
interesting picture.  @Fig:sines can also be referenced at the beginning of a
sentence with a different format.


# Tables

To build tables like @tbl:basic_table, any of the various normal markdown
syntaxes can be used.  The table can also include values taken from executed
code. @Tbl:basic_table has one of these in the lower right corner.

```{.python}
cell_value = 37
```

  Right     Left     Center     Default
-------     ------ ----------   --------------------
     12     12        12            12
    123     123       123          123
      1     1          1        `cell_value`{.python}

Table: Demonstration of simple table syntax. {#tbl:basic_table}

In addition there are helper functions in the Python library for building tables
from ordinary lists of items.  This is demonstrated in @tbl:computed_table.
Including the `.python` class makes the `print` statement executable and
captures the output which is Markdown.  Including the `.md` (markdown) class
then tells the Pandoc filter to convert the Markdown into document elements on
the fly rather than including the result verbatim.

```{.python}
from sciengdox.tables import Table
tbl = Table([['abc def', 'bcd', 'xyz'],
                ['egg', 'dog walker', 'guppy'],
                ['bird', 'octopus', 'cat food']],
            max_widths=[4, None, 4])
```

`print(tbl.markdown('my caption', 'tbl:computed_table', 'crl'))`{.python .md}


## Units

Units math is baked in through the inclusion of Pint.  This allows you to do
things like this:

```{.python .echo}
from sciengdox.units import Q_, ureg, pq
import sciengdox.constants as constants

mass = 10.0 * ureg('kg')
acceleration = constants.g
force = mass * acceleration
print(force.to('N'))
```

You can also print neat quantities (i.e. values with units) inline using the
`pq()`{.noexec} macro like this force value: `pq(force)`.
