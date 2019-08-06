---
title: Example Document
author: [Author]
date: 2019-08-06
subject: "Markdown"
tags: [Markdown, Example]
docnumber: XY-1234
docversion: 1
abstract: ["This is my wonderful medium-size abstract. Hello, here is some text without a meaning. This text should show what a printed text will look like at this place. If you read this text, you will get no information. Really? Is there no information?", "Another paragraph. Blah. Blah."]

compiledfrom: true
gitrepo: my_git_repo

titlepage: true
toc: true
lof: true
lot: true
lol: true

autoSectionLabels: true

natbib: true
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

# Section Headings

Hello, here is some text without a meaning. This text should show what a printed text will look
like at this place. If you read this text, you will get no information. Really? Is there no information?
Is there a difference between this text and some nonsense like “Huardest gefburn”? Kjift – not at all!
A blind text like this gives you information about the selected font, how the letters are written and an
impression of the look. This text should contain all letters of the alphabet and it should be written
in of the original language. There is no need for special content, but the length of words should match
the language.

Another paragraph in the first section.  Let's finish with a footnote.[^1]

On second thought, let's finish with a citation.  You should see Watson and Crick's article[@WatsonCrick1953].

On third thought, let's add an external link to [Google](http://google.com "Google").

On fourth thought, let's refer to another internal section like this: @Sec:minor-section.

[^1]: I'm a footnote!


## A Subsection

Hello, here is some text without a meaning. This text should show what a printed text will look
like at this place. If you read this text, you will get no information. Really? Is there no information?

### A Sub-subsection

Hello, here is some text without a meaning. This text should show what a printed text will look
like at this place. If you read this text, you will get no information. Really? Is there no information?

#### Minor section

Un-numbered short sections can also have a heading.

##### Paragraph Heading

Individual paragraphs can have headings too.

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

> Hello, here is some text without a meaning. This text should show what a printed text will look
> like at this place. If you read this text, you will get no information. Really? Is there no information?
> Hello, here is some text without a meaning. This text should show what a printed text will look
> like at this place. If you read this text, you will get no information. Really? Is there no information?
>
> 1. This is a list inside a block quote.
> 2. Second item.

# Figures

We can use Markdown for figures with captions and so on.

![Bender with Cigar](bender.png){#fig:bender width=50%}

Later, we can reference these figures. For instance, @fig:bender is an
interesting picture.  @Fig:bender can also be referenced at the beginning of a
sentence with a different format.

# Equations

Equations are important to be able to include and reference.

$$
y = -2.2x + 0.5
$$ {#eq:simple-equation}

@Eq:simple-equation is an interesting equation. We can, of course, link to
@eq:simple-equation.  And we can also inline math:  $y = ax + b$.

# Tables

Here is some bland text that now becomes interesting because it references
@tbl:my_table.  @Tbl:my_table is a capitalized link to the table.

  Right     Left     Center     Default
-------     ------ ----------   -------
     12     12        12            12
    123     123       123          123
      1     1          1             1

Table: Demonstration of simple table syntax. {#tbl:my_table}


# Code

This is where things get really interesting.

## Code Listings

Here is a simple code listing and a reference to it:  @lst:simple_listing.  @Lst:simple_listing is C++.
@Lst:simple_listing2 is Ruby.  Finally, @lst:simple_listing3 is Python

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

```{.python .echo}
class Greeter:
    def speak(__self__):
        print("Hello World")

greeter = Greeter()
greeter.speak()
```

# References
