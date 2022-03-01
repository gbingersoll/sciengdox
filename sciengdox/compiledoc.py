import argparse
from colorama import init as coloramaInit, Fore, Style
import glob
from pathlib import Path
import re
import shutil
import subprocess
import asyncio

coloramaInit(convert=True)


# print a colored error message
def print_error(msg):
    print(Fore.RED + msg + Style.RESET_ALL)


# find an executable on the system path or verify an explicit location
def find_executable(name, explicit_location):
    if explicit_location is not None:
        explicit_location = Path(explicit_location)
        if not explicit_location.exists():
            print_error(f"Could not find '{name}' at: {explicit_location.absolute()}")
            exit(-1)
        return explicit_location
    else:
        executable = shutil.which(name)
        if executable is None:
            print_error(f"Could not find '{name}' on system path.")
            exit(-1)
        return Path(executable)


# find a template file of the correct type in the provided path
def find_template_file(directory, basename, extension=None):
    extension = f".{extension}" if extension else ""
    if basename is None:
        search_files = list(directory.rglob(f"*{extension}"))
        if len(search_files) == 0:
            return None
        return search_files[0]
    else:
        template_file = directory.joinpath(f"{basename}{extension}")
        if not template_file.exists():
            print_error(f"File does not exist: {template_file.absolute()}")
            exit(-3)
        return template_file


# Copy template files to the output directory from which pandoc is run
def copy_template_to_output(template_dir, output_dir):
    if template_dir:
        print(Fore.CYAN + "Copying template files to output directory")
        template_files = template_dir.glob("*")
        for f in template_files:
            if f.is_file():
                shutil.copy(f, output_dir)


# Runs a shell command asynchronously
async def run(cmd, *args):
    proc = await asyncio.subprocess.create_subprocess_exec(
        cmd, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        stdout = stdout.decode()
    if stderr:
        stderr = stderr.decode()
    return proc.returncode, stdout, stderr


# checks if branch has something pending
def parse_git_dirty():
    code, stdout, stderr = asyncio.run(run("git", "diff", "--ignore-submodules"))
    if code == 0 and "" == stdout.strip():
        return False
    return True


# gets the current git branch
def parse_git_branch():
    code, stdout, stderr = asyncio.run(run("git", "branch", "--no-color"))
    if code != 0:
        return ""
    branch = re.search(r"^\*\s+(\w+)", stdout, re.MULTILINE).groups()[0]
    if parse_git_dirty():
        branch = "*" + branch

    return branch


# get last commit hash prepended with @ (i.e. @8a323d0)
def parse_git_hash():
    code, stdout, stderr = asyncio.run(run("git", "rev-parse", "--short", "HEAD"))
    if code != 0:
        return ""
    return "@" + stdout.strip()


def run_pandoc(params, output_path, verbose=False):
    completedProcess = subprocess.run(params, cwd=str(output_path), capture_output=True)
    if verbose:
        print(Fore.YELLOW + f"{completedProcess.stdout.decode()}")

    if completedProcess.returncode != 0:
        print(Fore.RED + f"{completedProcess.stderr.decode()}")
        exit(completedProcess.returncode)


# ------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Compile a Python-enabled document")
    parser.add_argument(
        "input_md", metavar="input_md", type=str, help="input markdown file"
    )
    parser.add_argument(
        "-o", "--output_dir", type=str, default="output", help="output directory"
    )
    parser.add_argument(
        "--template_dir", type=str, default="template", help="template directory"
    )
    parser.add_argument(
        "--images_dir",
        type=str,
        default="images",
        help="relative path to images directory",
    )
    parser.add_argument(
        "--template", type=str, help="name of template file (without extension)"
    )
    parser.add_argument(
        "--stylesheet", type=str, help="basename of css or scss stylesheet"
    )
    parser.add_argument(
        "--sass",
        type=str,
        help="full path to sass executable for converting stylesheet.  "
        "If omitted, system path is used",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="show verbose pandoc output",
    )
    parser.add_argument(
        "--self-contained",
        action="store_true",
        default=False,
        help="generate self-contained HTML output",
    )
    parser.add_argument(
        "--statics",
        type=str,
        default=["*.bib*"],
        nargs="*",
        help="patterns of other files needed by pandoc in the "
        "output directory (e.g. *.bib*)",
    )

    md_group = parser.add_mutually_exclusive_group()
    md_group.add_argument(
        "--md",
        action="store_true",
        default=False,
        help="build intermediate markdown output",
    )
    md_group.add_argument(
        "--no-md", action="store_true", help="do not build intermediate markdown output"
    )
    html_group = parser.add_mutually_exclusive_group()
    html_group.add_argument(
        "--html", action="store_true", default=False, help="build HTML output"
    )
    html_group.add_argument(
        "--no-html", action="store_true", help="do not build HTML output"
    )
    pdf_group = parser.add_mutually_exclusive_group()
    pdf_group.add_argument(
        "--pdf", action="store_true", default=False, help="build PDF output"
    )
    pdf_group.add_argument(
        "--no-pdf", action="store_true", help="do not build PDF output"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="build all output formats (can be combined with --no-<format>)",
    )
    parser.add_argument(
        "--pandoc",
        type=str,
        help="full path to pandoc executable.  " "If omitted, system path is used",
    )
    parser.add_argument(
        "--pandoc-pythonexec",
        type=str,
        help="full path to pandoc-pythonexec filter.  "
        "If omitted, system path is used",
    )
    parser.add_argument(
        "--pandoc-crossref",
        type=str,
        help="full path to pandoc-crossref filter.  " "If omitted, system path is used",
    )
    parser.add_argument(
        "--pandoc-citeproc",
        type=str,
        help="full path to pandoc-citeproc filter.  " "If omitted, system path is used",
    )
    parser.add_argument(
        "--use-pandoc-citeproc",
        action="store_true",
        default=False,
        help="whether to use the older pandoc-citeproc filter.  If false "
        "(default), the --citeproc flag is used instead.",
    )
    parser.add_argument(
        "--no-citeproc",
        action="store_true",
        default=False,
        help="whether to run citation processing",
    )

    args = parser.parse_args()

    # Check for required utilities
    pandoc_exec = find_executable("pandoc", args.pandoc)
    pandoc_pythonexec = find_executable("pandoc-pythonexec", args.pandoc_pythonexec)
    pandoc_citeproc = None
    if args.use_pandoc_citeproc and not args.no_citeproc:
        pandoc_citeproc = find_executable("pandoc-citeproc", args.pandoc_citeproc)
    pandoc_crossref = find_executable("pandoc-crossref", args.pandoc_crossref)

    # Check specified outputs
    build_md = (args.md or args.all) and not args.no_md
    build_html = (args.html or args.all) and not args.no_html
    build_pdf = (args.pdf or args.all) and not args.no_pdf
    if not (build_md or build_html or build_pdf):
        print(Fore.YELLOW + "No output specified.  Building HTML.")
        build_html = True

    # Build paths to inputs, outputs, templates
    input_md = Path(args.input_md)
    if not input_md.exists():
        print_error(f"Input file does not exist: {args.input_md}")

    input_basename = input_md.stem

    template_dir = Path(args.template_dir)

    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True)
        print(Fore.BLUE + f"Creating output directory: {output_dir.absolute()}")
    except FileExistsError:
        print(Fore.BLUE + f"Using output directory: {output_dir.absolute()}")

    # Copy static images to output directory
    images_dir = Path(args.images_dir)
    if images_dir.exists():
        print(
            Fore.BLUE
            + "Copying images to output directory from: "
            + f"{images_dir.absolute()}"
        )

        output_images = output_dir.joinpath(images_dir.name)

        shutil.copytree(
            images_dir.absolute(), output_images.absolute(), dirs_exist_ok=True
        )

    # Copy other specified static files to output directory
    static_files = []
    for g in args.statics:
        path = Path(g)
        static_files += list(map(lambda f: Path(f), glob.glob(f"{path.absolute()}")))
    if len(static_files) > 0:
        print(Fore.BLUE + "Copying static files to output directory:")
        for f in static_files:
            print(f"    {f}")
            if f.is_dir():
                result_dir = output_dir.joinpath(f.name)
                shutil.copytree(f.absolute(), result_dir.absolute(), dirs_exist_ok=True)
            else:
                shutil.copy(f.absolute(), output_dir.absolute())

    common_pandoc_params = [
        str(pandoc_exec.absolute()),
        str(input_md.absolute()),
        "--from",
        "markdown",
        "-Mcref",
        "-Mlistings",
        f"-Mgithash={parse_git_branch()}{parse_git_hash()}",
        "--filter",
        str(pandoc_pythonexec.absolute()),
        "--filter",
        str(pandoc_crossref.absolute()),
    ]

    if not args.no_citeproc:
        if pandoc_citeproc:
            common_pandoc_params += [
                "--filter",
                str(pandoc_citeproc.absolute()),
            ]
        else:
            common_pandoc_params += ["--citeproc"]

    if build_md:
        # Build Markdown output
        output_file = output_dir.joinpath(input_basename + ".md")
        print(Fore.BLUE + "Building Markdown output: " + f"{output_file.absolute()}")

        copy_template_to_output(template_dir, output_dir)
        print(Fore.CYAN + "Running pandoc")
        pandoc_params = common_pandoc_params + [
            "--output",
            str(output_file.absolute()),
        ]
        run_pandoc(pandoc_params, output_dir, verbose=args.verbose)

    if build_html:
        # Build HTML output
        output_file = output_dir.joinpath(input_basename + ".html")
        print(Fore.BLUE + f"Building HTML output: {output_file.absolute()}")

        template_file = find_template_file(template_dir, args.template, "html")
        if template_file is None:
            print(
                Fore.YELLOW
                + "Did not find an HTML template in: "
                + f"{template_dir.absolute()}"
            )
        else:
            print(Fore.CYAN + f"Using template: {template_file.absolute()}")

        # Look for SCSS or CSS style file in the template directory
        stylesheet_file = find_template_file(template_dir, args.template, "scss")
        if stylesheet_file is not None:
            sass_exec = find_executable("sass", args.sass)
            infile = stylesheet_file
            stylesheet_file = output_dir.joinpath(f"{infile.stem}.css")
            print(Fore.CYAN + "Converting SCSS to CSS")
            subprocess.run(
                [
                    str(sass_exec.absolute()),
                    str(infile.absolute()),
                    str(stylesheet_file.absolute()),
                    "--style",
                    "compressed",
                ]
            )
        else:
            stylesheet_file = find_template_file(template_dir, args.template, "css")
            if stylesheet_file:
                shutil.copy(stylesheet_file, output_dir)

        if stylesheet_file:
            stylesheet_file = stylesheet_file.name

        copy_template_to_output(template_dir, output_dir)

        print(Fore.CYAN + "Running pandoc")

        pandoc_params = common_pandoc_params + [
            "--output",
            str(output_file.absolute()),
            "--listings",
            "--toc",
            "--number-sections",
            "--mathjax",
            "-Mcolorlinks",
            "-MlinkReferences",
            "-Mlink-citations",
        ]

        if template_file:
            pandoc_params.append("--template")
            pandoc_params.append(template_file.stem)
        if stylesheet_file:
            pandoc_params.append(f"-Mcss={stylesheet_file}")
        if args.verbose:
            pandoc_params.append("--verbose")
        if args.self_contained:
            pandoc_params.append("--self-contained")

        run_pandoc(pandoc_params, output_dir, verbose=args.verbose)

        # Post-process HTML file to incorporate e.g. interactive Plotly images
        from bs4 import BeautifulSoup

        with open(output_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for img in soup.find_all(src="broken_img_replace_me"):
            div = soup.find(
                lambda tag: tag.name == "div"
                and tag.has_attr("id")
                and tag["id"] == img["id"]
            )
            img.replace_with(div.extract())
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(soup))

    if build_pdf:
        # Build PDF output
        output_file = output_dir.joinpath(input_basename + ".pdf")
        print(Fore.BLUE + f"Building PDF output: {output_file.absolute()}")

        template_file = find_template_file(template_dir, args.template, "latex")
        if template_file is None:
            print(
                Fore.YELLOW
                + "Did not find a LaTeX template in: "
                + f"{template_dir.absolute()}"
            )
        else:
            print(Fore.CYAN + f"Using template: {template_file.absolute()}")

        copy_template_to_output(template_dir, output_dir)

        print(Fore.CYAN + "Running pandoc")

        pandoc_params = common_pandoc_params + [
            "--output",
            str(output_file.absolute()),
            "--pdf-engine",
            "xelatex",
            "--listings",
            "--toc",
            "--number-sections",
            "-Mcolorlinks",
        ]

        if template_file:
            pandoc_params.append("--template")
            pandoc_params.append(template_file.stem)
        if args.verbose:
            pandoc_params.append("--verbose")

        run_pandoc(pandoc_params, output_dir, verbose=args.verbose)

    print(Fore.GREEN + "Complete")
    print(Style.RESET_ALL)
