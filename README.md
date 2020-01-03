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

# Use and Example

An example Pandoc markdown file can be found in `example`.  To process this
file, you need to have [`pandoc`](https://pandoc.org/) installed and in your
path.  You also need to install the Pandoc filters
[pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) and
[pandoc-citeproc](https://github.com/jgm/pandoc-citeproc) which provide nice
cross-referencing and reference/bibliography handling.

## Installation

When working with macOS or Linux or
[Linux on Windows via WSL](https://gist.github.com/gbingersoll/9e18afb9f4c3acd8674f5595c7e010f5)
`pandoc` and the filters can be installed via [Homebrew](https://brew.sh/).  (On
Linux/WSL, install [linuxbrew](https://docs.brew.sh/Homebrew-on-Linux).)  Then
simply run:

```shell
$ brew install pandoc
$ brew install pandoc-crossref
$ brew install pandoc-citeproc
```

Then, of course, you need to install this filter and some other helpers for the
example.  The example helpers can be installed into your Python virtual
environment by running:

```shell
$ pipenv install -e .[examples]
```

### PDF Generation

To generate PDF files through Pandoc, you need to have `xelatex` installed.
On Linux/WSL:

```shell
$ sudo apt-get install texlive-xetex
```

On macOS:

```shell
$ brew cask install mactex
```

### Fonts

The example templates rely on having a few fonts installed.
The fonts to get are the Google
[Source Sans Pro](https://fonts.google.com/specimen/Source+Sans+Pro),
[Source Code Pro](https://fonts.google.com/specimen/Source+Code+Pro), and
[Source Serif Pro](https://fonts.google.com/specimen/Source+Serif+Pro) families.

On macOS, these can simply be downloaded and installed as you would any other
font.  On Linux via WSL, you can install these normally on the Windows side and
then synchronize the Windows font folder to the Linux side.  To do this, edit
(using `sudo`) `/etc/fonts/local.conf` and add:

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
    <dir>/mnt/c/Windows/Fonts</dir>
</fontconfig>
```

Then update the font cache on the Linux side:

```shell
$ sudo fc-cache -fv
```

### Stylesheets

The example file uses an HTML template that includes a CSS stylesheet that is
generated from [SCSS](https://sass-lang.com/documentation/syntax).  To compile
this automatically, you need to have
[SASS installed](https://sass-lang.com/install).

On macOS, this can be installed via Homebrew:

```shell
$ brew install sass/sass/sass
```

On macOS/Linux/WSL it can be installed as a Node.js package (assuming you
already have [Node.js/npm](https://nodejs.org/) installed):

```shell
$ npm install -g sass
```

## Building

This Python library provides a script, `compiledoc`, that will appear in your
virtual environment's path once the library is installed.  In general, you
provide an output directory and an input markdown file, and it will build an
HTML output when the `--html` flag is used (also by default).

```shell
$ compiledoc -o output --html mydoc.md
```

To build a PDF (via `xelatex`):

```shell
$ compiledoc -o output --pdf mydoc.md
```

To build a Markdown file with executable Python output included (e.g. for
debugging purposes), specify `--md`.  This will generate a file in the output
directory with (perhaps confusingly) the same name as the input:

```shell
$ compiledoc -o output --md mydoc.md
```

To build everything, specify `--all`:

```shell
$ compiledoc -o output --all mydoc.md
```

To see all available command line options (for specifying templates, paths to
required external executables, static files like images and bibliography files,
etc.):

```shell
$ compiledoc --help
```

## Building the Example

Once everything is setup, compile the example HTML file by running:

```shell
$ cd example
$ compiledoc -o output example.md
```

Open `example/output/example.html` in your browser or use e.g. the [Live
Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
plugin for VS Code.

## Auto Regen

To autoregenerate the document (e.g. the HTML version, the output of which is
watched by the
[Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
), you can use [Watchman](https://facebook.github.io/watchman/).

To create a trigger on a particular directory (`doc/` in this example) with a
`notebook.md` file (change this to suit your purposes), copy the following into
a temporary `trigger.json` file:

```json
[
    "trigger",
    "doc/",
    {
        "name": "build_html",
        "expression": [
            "anyof",
            [
                "match",
                "notebook.md",
                "wholename"
            ]
        ],
        "command": [
            "pipenv",
            "run",
            "compiledoc",
            "-o",
            "output",
            "--html",
            "notebook.md"
        ]
    }
]
```

Then from your project root directory run:

```shell
watchman -j < trigger.json
rm trigger.json
```

It is also recommended that you add a `.watchmanconfig` file to the watched
directory (e.g. `doc/`; also add `.watchmanconfig` to your `.gitignore`) with
the following contents:

```json
{
  "settle": 3000
}
```

The settle parameter is in milliseconds.

To turn off watchman:

```shell
watchman shutdown-server
```

To turn it back on:

```shell
cd <project-root>
watchman watch doc/
```

To watch the Watchman:

```shell
tail -f /usr/local/var/run/watchman/<username>-state/log
```

(Note that on Windows/WSL, to get `tail` to work the way you expect, you need to
add `---disable-inotify` to the command; and yes, that's three `-` for some
reason.)

