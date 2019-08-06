# sciengdox

A python package for creating scientific and engineering documents
via pandoc including inline-executable Python code.


## Key Features

1. Pandoc filter for converting pandoc markdown to other formats (especially
   HTML and PDF).
2. Codeblock execution
3. Helper functions for generating tables, SVG matplotlib plots, etc.
4. Code execution results caching


# Motivation

This is inspired by pweave, codebraid, knitr, and friends, but I always seemed
to have to do some pre/post-processing to get things the way I want them.  I
already use other pandoc filters (e.g. pandoc-citeproc, pandoc-crossref), so why
not simply have another pandoc filter that will execute inline code and insert
the results.

Another key is getting quality diagrams from scientific python code.  For
example, pweave automatically inserts generated images, but there doesn't seem
to be a way to get SVG images without, again, pre- and post-processing in
another script.  SVG plots are, obviously, scalable and work much better for web
and PDF outputs.


# Development

Use pipenv for environment management.  After cloning the repository:

```shell
$ cd <project-repo>
$ pipenv install -e .[tests]
$ pipenv shell
```
