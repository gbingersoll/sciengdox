# sciengdox

A python package for creating scientific and engineering documents
via pandoc including inline-executable Python code.


## Key Features

1. [Pandoc filter](https://pandoc.org/filters.html) for converting pandoc
   markdown to other formats (especially HTML and PDF).
2. Codeblock execution
3. Helper functions for generating tables, SVG
   [matplotlib](https://matplotlib.org/) plots, etc.
4. Code execution results caching


# Motivation

This is inspired by [`pweave`](http://mpastell.com/pweave/),
[`codebraid`](https://github.com/gpoore/codebraid),
[`knitr`](https://yihui.name/knitr/), and cousins, but I always seemed to have
to do some pre/post-processing to get things the way I want them.  I already use
other pandoc filters (e.g. pandoc-citeproc, pandoc-crossref), so why not simply
have another pandoc filter that will execute inline code and insert the results.

Another key is getting quality diagrams from scientific python code.  For
example, pweave automatically inserts generated images, but there doesn't seem
to be a way to get SVG images without, again, pre- and post-processing in
another script.  SVG plots are, obviously, scalable and work much better for web
and PDF outputs.


# Development

Use [`pipenv`](https://docs.pipenv.org/) for local environment management.
After cloning the repository:

```shell
$ cd <project-repo>
$ pipenv install -e .[tests]
$ pipenv shell
```


# Example

An example Pandoc markdown file can be found in `example`.  To process this
file, you need to have [`pandoc`](https://pandoc.org/) installed and in your
path.  You also need to install the Pandoc filters
[pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) and
[pandoc-citeproc](https://github.com/jgm/pandoc-citeproc).

The example also requires some python scientific modules.  Install these in your
virtual environment by running:

```shell
$ pipenv install -e .[examples]
```

Then compile the example HTML file by running:

```shell
$ cd example
$ ./build.sh
```

Open `example/output/example.html` in your browser or use e.g. the [Live
Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
plugin for VS Code.
