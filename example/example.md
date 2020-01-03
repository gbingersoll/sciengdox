---
title: Example Document
author: [Author]
date: 2019-12-30
subject: "Markdown"
tags: [Markdown, Example]
docnumber: XY-1234
docversion: 1
abstract: ["This is my wonderful medium-size abstract. Hello, here is some text without a meaning. This text should show what a printed text will look like at this place. If you read this text, you will get no information. Really? Is there no information?", "Another paragraph. Blah. Blah."]

compiledfrom: true
gitrepo: my_git_repo

titlepage: true
lof: true
lot: true
lol: true

autoSectionLabels: true

bibliography: example.bib
csl: ieee.csl
references:
- type: article-journal
  id: WatsonCrick1953
  author:
  - family: Watson
    given: J. D.
  - family: Crick
    given: F. H. C.
  issued:
    date-parts:
    - - 1953
      - 4
      - 25
  title: 'Molecular structure of nucleic acids: a structure for deoxyribose
    nucleic acid'
  title-short: Molecular structure of nucleic acids
  container-title: Nature
  volume: 171
  issue: 4356
  page: 737-738
  DOI: 10.1038/171737a0
  URL: http://www.nature.com/nature/journal/v171/n4356/abs/171737a0.html
  language: en-GB
...

# Example Document

This document demonstrates some available features for your writing.  Mostly it
is everything in standard [Pandoc Markdown](https://pandoc.org/MANUAL.html#pandocs-markdown)
with some additional conventions.

Of particular interest, though, are executable code blocks discussed in
@sec:code-execution.

# Section Headings

This is a major section.

## A Subsection

This is a subsection.

### A Sub-subsection

This is a sub-subsection.

#### Minor section

Un-numbered short sections can also have a heading.  Note that in LaTeX terms,
this is actually a "paragraph".

##### Paragraph Heading

Individual paragraphs can have headings too.  In LaTeX terms, this is actually a
sub-paragraph. These may not actually be terribly useful.

# Links

Links to internal sections are handled using the
[`pandoc-crossref`](https://lierdakil.github.io/pandoc-crossref/) filter.  You
can reference sections as in @sec:minor-section.  @Sec:a-subsection demonstrates a
link starting a sentence.  Setting up styles (e.g. "sec." or "section") happens
in the file `pandoc-crossref.yaml` in the template subdirectory.

You can also generate external links with hover text like this:
[Google](http://google.com "Google").

# Citations

Citations are handled using the
[`pandoc-citeproc`](https://github.com/jgm/pandoc-citeproc/) filter.  Citation
data is entered as metadata at the top of the markdown file, and you can
reference an article in the text[@WatsonCrick1953].

You can also put your references in a [BibTeX](http://www.bibtex.org/) file or
any of the other file formats that `pandoc-citeproc` supports.  This citation
comes from the `example.bib` file[@mrx05].  The bibliography file name can be
provided in the metatdata at the top of the markdown file.

Formatting of citations is handled via a `.csl` file.  The one for
[IEEE style](https://ieee-dataport.org/sites/default/files/analysis/27/IEEE%20Citation%20Guidelines.pdf)
is used in this example.

# Footnotes

This paragraph has a linked footnote[^1] that will appear in the document.

[^1]: I'm a footnote!

# Lists

Here are the styles for ordered and unordered lists.

* One
* Two
    * Nested one
* Three
    1. Numerated list
    1. No need to specify number

If lists are spaced in the markdown, they get spread out in the output file.

* One

* Two
    * Nested one

Lists can include multiple paragraphs:

* One

  New paragraph within first item
* Two

Finally, there are definition lists that are useful for glossaries and such.

Term 1
:   Definition 1

Term 2
:   Definition 2.  This definition is much longer to show how line breaks and
    formatting work.  Once the line breaks we can see what it looks like.

Term 3
:   Definition 2

# Block Quotes
Block quotes are useful for including relevant information directly in the
document rather than only including a citation.

> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
> incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
> nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
> Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
> fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
> culpa qui officia deserunt mollit anim id est laborum.
>
> 1. This is a list inside a block quote.
> 2. Second item.

# Equations

Equations are important to be able to include and reference.

$$
y = -2.2x + 0.5
$$ {#eq:simple-equation}

@Eq:simple-equation is an interesting equation. We can, of course, link to
@eq:simple-equation.  And we can also inline math:  $y = ax + b$.

# Code

This is where things get really interesting.

## Code Listings

Here is a simple code listing and a reference to it:  @lst:simple_listing.  @Lst:simple_listing is C++.
@Lst:simple_listing2 is Ruby.  Finally, @lst:simple_listing3 is Python.

We can also put `code keywords` inline with regular text.

```{#lst:simple_listing .cpp caption="Listing of C++ code"}
// A simple class
class Hello {
public:
  void go(void) {
    printf("Hello World\n");
  }
}
```

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

## Code Execution

Defining this code block will echo the code block itself to the document and
also will execute it, printing the output to the document as well.
@Lst:executed_python is executed python code.

```{.python .echo #lst:executed_python caption="Executed Python code"}
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

In general, a code block with the `.python` flag will be executed unless it also
includes the `.noexec` flag.  If the `.echo` flag is included, the block and the
results will be inclued in the document.

@Lst:continued_python continues from the previous one, so variables stay
defined.  This code block also includes the `.repl` flag which simulates an
interactive session by prefixing inputs with `>>>`.

```{.python .echo .repl #lst:continued_python caption="Executed Python code continuing from the previous block and displayed like a REPL session"}
greeter.respond("Joe")
greeter.respond("Joe", polite=True)
```

```{.python}
my_value = 37
```

The block right above this one in the markdown is not printed (because it does
not included the `.echo` flag), but it establishes the value
`my_value`{.python}.  This defaults to printing as plain text to match the
surrounding paragraph, but you can also keep a result formatted as monospace
code by including `.asCode` in its classes like this: `2*my_value`{.python
.asCode}.  You can also wrap the result in an equation like
$3x=`3*my_value`{.python}$.  This works for equation blocks too as in
@eq:equation-with-code-eval.

$$
y = -5x + 0.5 = `-5 * my_value + 0.5`{.python}
$$ {#eq:equation-with-code-eval}

# Figures

We can use Markdown for figures with captions and so on.  Static images should
be stored in a subfolder `images/`.  This folder gets copied to the specified
output directory when the document is compiled.  (Subfolders within the that
folder are, of course, allowed for organization.)

![A Dog. (Photo by [Jamie Street](https://unsplash.com/@jamie452) on [Unsplash](https://unsplash.com))](images/jamie-street-UtrE5DcgEyg-unsplash.jpg){#fig:dog width=50%}

Later, we can reference these figures. For instance, @fig:dog is an
interesting picture.  @Fig:dog can also be referenced at the beginning of a
sentence with a different format.

We can also generate figures through code execution.

```{.python .echo #lst:image_gen_python caption="Executed Python code generating an image"}
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

Later, we can reference these generated figures, too. For instance, @fig:sines
is an interesting picture.  @Fig:sines can also be referenced at the beginning
of a sentence with a different format.

# Units

Units math is baked in through the inclusion of
[Pint](https://pint.readthedocs.io/en/0.9/).  This allows you to do things like
this:

```{.python .echo .repl #lst:units_python caption="Executed Python using units math"}
from sciengdox.units import Q_, ureg, pq
import sciengdox.constants as constants

mass = 10.0 * ureg('kg')
acceleration = constants.g
force = mass * acceleration
print(force.to('N'))
```

You can also print neat quantities (i.e. values with units) inline using the
`pq()`{.noexec} macro like this force value: `pq(force)`.

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

`print(tbl.markdown('A Computed Table', 'tbl:computed_table', 'crl'))`{.python .md}

One catch with the way the interpreter works means that if your Python-built
table has footnotes, you need to define them in Python code and not directly
in the Markdown file.  Like this:

```{.python .echo #lst:table_with_footnotes caption="Python for building a table with footnotes"}
from sciengdox.tables import Table
tbl = Table([['abc def', 'bcd', 'xyz'],
             ['egg[^eggNote]', 'dog walker', 'guppy'],
             ['bird[^birdNote]', 'octopus', 'cat food']],
            max_widths=[4, None, 4])
notes = {
    'eggNote': "A very young bird",
    'birdNote': "An old egg"
}
tbl_markdown = tbl.markdown('A Computed Table with Footnotes',
                            'tbl:computed_table_with_notes',
                            'crl',
                            footnotes=notes)
```

`print(tbl_markdown)`{.python .md}

# References
