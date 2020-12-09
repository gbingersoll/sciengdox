# sciengdox

A python package for creating scientific and engineering documents
via [`pandoc`](https://pandoc.org/) including inline-executable Python code.


## Key Features

1. [Pandoc filter](https://pandoc.org/filters.html) for converting pandoc
   markdown to other formats (especially HTML and PDF).
2. Codeblock execution
3. Helper functions for generating tables, SVG
   [matplotlib](https://matplotlib.org/) plots, etc.


# Motivation

This is inspired by [`pweave`](http://mpastell.com/pweave/),
[`codebraid`](https://github.com/gpoore/codebraid),
[`knitr`](https://yihui.name/knitr/), and cousins, but I always seemed to have
to do some pre/post-processing to get things the way I want them.  I already use
other pandoc filters (e.g. pandoc-citeproc, pandoc-crossref), so why not simply
have another pandoc filter that will execute inline code and insert the results?

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
$ pipenv install -e .[dev]
$ pipenv shell
```

To package and release, from within the virtual environment:

```shell
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```

See also [this page](https://packaging.python.org/tutorials/packaging-projects/).

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
$ brew install librsvg
```

Then, of course, you need to install this filter and some other helpers for the
example.  The example helpers can be installed into your Python virtual
environment by running:

```shell
$ pipenv install -e .[examples]
```

### Windows-specific Install

To set up an environment for Windows from scratch including terminals, editors,
Python, etc., see
[this gist](https://gist.github.com/gbingersoll/c3033f8cb41c3eb865563c0711a30545).
Additional installation steps to use this library include installing `pandoc`
and additional filters and utilities.

Install `pandoc` by [downloading the installer](https://pandoc.org/installing.html)
and following the standard instructions.  This should also get you
`pandoc-citeproc.exe` for managing citations.

Install `pandoc-crossref` (for managing intra-document cross-references) by
[downloading](https://github.com/lierdakil/pandoc-crossref/releases) the zipped
Windows release.  Unzip it, and move `pandoc-crossref.exe` to a location that is
on your system path.  For example, you can move to next to `pandoc-citeproc.exe`
in `C:\Program Files\Pandoc`.

Finally, to handle embedding SVG images in PDF documents, this library relies on
`rsvg-convert`.  This can be installed via
[Chocolatey](https://chocolatey.org/).  Install the Chocolatey package manager
if you do not already have it, and then run:

```shell
$ choco install rsvg-convert
```

Instead of (or in addition to) Chocolately, you can also install the
[Scoop](https://scoop.sh/) installer.  Scoop does not currently have a formula
for `rsvg-convert`, but it can also be installed from
[SourceForge](https://sourceforge.net/projects/tumagcc/files/rsvg-convert-dll-2.40.16.7z/download?use_mirror=phoenixnap)
if you do not want to use Chocolatey.


#### UTF-8 Note

The underlying Pandoc filter for executing Python code embedded in your
documents relies on inter-process communication with a Python REPL behind the
scenes.  The default inter-process character encoding for Python on Windows is
[CP-1252](https://en.wikipedia.org/wiki/Windows-1252), and this can cause
problems if your Python scripts generate output with special characters (and if
you are doing any scientific or engineering writing, they definitely will).

Fortunately, this is easily worked-around by setting a Windows environment
variable `PYTHONIOENCODING` to `utf-8`.  After setting this, be sure to restart
any open terminal windows for the change to take effect.

#### Matplotlib Note

If you use `matplotlib` for generating plots in inline Python code in your
document, you should explicity set the `Agg` backend early in your document (see
the `example/example.md` in this repo).  Without this, document conversion can
hang when the `svg_figure` helper function is called.

Somewhere near the top of your Markdown document, add an executable Python code
block (without `.echo` so it won't appear in the output) that includes:

```python
import matplotlib
matplotlib.use('Agg')
```

#### Panflute Version Note

This plugin relies on the
[`panflute`](https://github.com/sergiocorreia/panflute) Python package as a
bridge between Python and `pandoc`'s Haskell.  The `panflute`
[README](https://github.com/sergiocorreia/panflute#supported-pandoc-versions)
lists API compatibility requirements between versions of `panflute` and versions
of `pandoc`.  Double-check this if you run into errors that mention `panflute`
when compiling a document.

If you are running an older version of `pandoc` (e.g. 2.9.2) and start a new
project, you will need to explicitly install the compatible `panflute` version
in your environment with e.g. `pipenv install panflute==1.12.5`.  Or
alternatively install a `pandoc` version 2.11.x.

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

On Windows (without WSL):

[Download the MikTeX installer](https://miktex.org/download) and install as
usual.  Then ensure that the binary folder is in your path (e.g. 
`C:\Users\<username>\AppData\Local\Programs\MiKTeX 2.9\miktex\bin\x64\`).  Note
that the first time you generate a document, MikTex will prompt you to install a
lot of packages, so watch for a MikTeX window popping up (possibly behind other
windows) and follow the prompts.


### Fonts

The example templates rely on having a few fonts installed.
The fonts to get are the Google
[Source Sans Pro](https://fonts.google.com/specimen/Source+Sans+Pro),
[Source Code Pro](https://fonts.google.com/specimen/Source+Code+Pro), and
[Source Serif Pro](https://fonts.google.com/specimen/Source+Serif+Pro) families.

On macOS or Windows (without WSL), these can simply be downloaded and installed
as you would any other font.  On Linux via WSL, you can install these normally
on the Windows side and then synchronize the Windows font folder to the Linux
side.  To do this, edit (using `sudo`) `/etc/fonts/local.conf` and add:

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

On macOS/Linux/WSL/Windows it can be installed as a Node.js package (assuming
you already have [Node.js/npm](https://nodejs.org/) installed):

```shell
$ npm install -g sass
```

## Building

This Python library provides a script, `compiledoc`, that will appear in your
`pipenv` virtual environment's path once the library is installed.  In general,
you provide an output directory and an input markdown file, and it will build an
HTML output when the `--html` flag is used (and also by default).

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

## Older pandoc Versions

For `pandoc` 2.9 and earlier, the citation manager `pandoc-citeproc` was a
separate filter that gets added to the compliation pipeline.  The path to this
filter can be specified on the command line to `compiledoc` with the
`--pandoc-citeproc PATH` flag.

In newer versions of `pandoc` (2.11 and beyond), the citeproc filter is built-in
to pandoc and is run by adding `--citeproc` to the `pandoc` command-line.  The
`compiledoc` script adds this by default unless the flag `--use-pandoc-citeproc`
is added, in which case the older filter will be used.

If you do not with to run `citeproc` at all, you can add the flag
`compiledoc --no-citeproc` to skip citation processing altogether.
