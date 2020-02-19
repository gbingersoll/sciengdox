import argparse
from colorama import init as coloramaInit, Fore, Back, Style
import glob
import os
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
        if not os.path.isabs(explicit_location):
            explicit_location = os.path.join(os.getcwd(), explicit_location)
        if not os.path.exists(explicit_location):
            print_error(f'Could not find \'{name}\' at: {explicit_location}')
            exit(-1)
        return explicit_location
    else:
        executable = shutil.which(name)
        if executable is None:
            print_error(f'Could not find \'{name}\' on system path.')
            exit(-1)
        return executable


# find a template file of the correct type in the provided path
def find_template_file(directory, basename, extension=None):
    extension = f'.{extension}' if extension else ''
    if basename is None:
        search_files = glob.glob(os.path.join(
                                     directory,
                                     '**',
                                     f'*{extension}'),
                                 recursive=True)
        if len(search_files) == 0:
            return None
        return search_files[0]
    else:
        template_file = os.path.join(directory, f'{basename}{extension}')
        if not os.path.exists(input_md):
            print_error(f'File does not exist: {template_file}')
            exit(-3)
        return template_file


# Runs a shell command asynchronously
async def run(cmd, *args):
    proc = await asyncio.subprocess.create_subprocess_exec(
        cmd,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT)
    stdout, stderr = await proc.communicate()
    if stdout:
        stdout = stdout.decode()
    if stderr:
        stderr = stderr.decode()
    return proc.returncode, stdout, stderr


# checks if branch has something pending
def parse_git_dirty():
    code, stdout, stderr = asyncio.run(run('git',
                                           'diff',
                                           '--ignore-submodules'))
    if code == 0 and "" == stdout.strip():
        return False
    return True


# gets the current git branch
def parse_git_branch():
    code, stdout, stderr = asyncio.run(run('git', 'branch', '--no-color'))
    if code != 0:
        return ''
    branch = re.search(r"^\*\s+(\w+)", stdout, re.MULTILINE).groups()[0]
    if parse_git_dirty():
        branch = "*" + branch

    return branch


# get last commit hash prepended with @ (i.e. @8a323d0)
def parse_git_hash():
    code, stdout, stderr = asyncio.run(run('git',
                                           'rev-parse',
                                           '--short',
                                           'HEAD'))
    if code != 0:
        return ''
    return "@" + stdout.strip()


def run_pandoc(params, output_dir, verbose=False):
    completedProcess = subprocess.run(params,
                                      cwd=output_dir,
                                      capture_output=True)
    if verbose:
        print(Fore.YELLOW + f'{completedProcess.stdout.decode()}')

    if completedProcess.returncode != 0:
        print(Fore.RED + f'{completedProcess.stderr.decode()}')
        exit(completedProcess.returncode)


# ------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Compile a Python-enabled document')
    parser.add_argument('input_md', metavar='input_md', type=str,
                        help='input markdown file')
    parser.add_argument('-o', '--output_dir', type=str, default='output',
                        help='output directory')
    parser.add_argument('--template_dir', type=str, default='template',
                        help='template directory')
    parser.add_argument('--images_dir', type=str, default='images',
                        help='relative path to images directory')
    parser.add_argument('--template', type=str,
                        help='name of template file (without extension)')
    parser.add_argument('--stylesheet', type=str,
                        help='basename of css or scss stylesheet')
    parser.add_argument(
        '--sass', type=str,
        help='full path to sass executable for converting stylesheet.  '
            'If omitted, system path is used')
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='show verbose pandoc output')
    parser.add_argument(
        '--self-contained', action='store_true', default=False,
        help='generate self-contained HTML output')
    parser.add_argument(
        '--statics', type=str, default=['*.bib'], nargs='*',
        help='patterns of other files needed by pandoc in the '
            'output directory (e.g. *.bib)')

    md_group = parser.add_mutually_exclusive_group()
    md_group.add_argument('--md', action='store_true', default=False,
                            help='build intermediate markdown output')
    md_group.add_argument('--no-md', action='store_true',
                            help='do not build intermediate markdown output')
    html_group = parser.add_mutually_exclusive_group()
    html_group.add_argument('--html', action='store_true', default=False,
                            help='build HTML output')
    html_group.add_argument('--no-html', action='store_true',
                            help='do not build HTML output')
    pdf_group = parser.add_mutually_exclusive_group()
    pdf_group.add_argument('--pdf', action='store_true', default=False,
                        help='build PDF output')
    pdf_group.add_argument('--no-pdf', action='store_true',
                        help='do not build PDF output')
    parser.add_argument(
        '--all', action='store_true', default=False,
        help='build all output formats (can be combined with --no-<format>)')
    parser.add_argument(
        '--pandoc', type=str,
        help='full path to pandoc executable.  '
            'If omitted, system path is used')
    parser.add_argument(
        '--pandoc-pythonexec', type=str,
        help='full path to pandoc-pythonexec filter.  '
            'If omitted, system path is used')
    parser.add_argument(
        '--pandoc-crossref', type=str,
        help='full path to pandoc-crossref filter.  '
            'If omitted, system path is used')
    parser.add_argument(
        '--pandoc-citeproc', type=str,
        help='full path to pandoc-citeproc filter.  '
            'If omitted, system path is used')

    args = parser.parse_args()

    # Check for required utilities
    pandoc_exec = find_executable('pandoc', args.pandoc)
    pandoc_pythonexec = find_executable('pandoc-pythonexec',
                                        args.pandoc_pythonexec)
    pandoc_citeproc = find_executable('pandoc-citeproc', args.pandoc_citeproc)
    pandoc_crossref = find_executable('pandoc-crossref', args.pandoc_crossref)

    # Check specified outputs
    build_md = (args.md or args.all) and not args.no_md
    build_html = (args.html or args.all) and not args.no_html
    build_pdf = (args.pdf or args.all) and not args.no_pdf
    if not (build_md or build_html or build_pdf):
        print(Fore.YELLOW + "No output specified.  Building HTML.")
        build_html = True

    # Build absolute paths to inputs, outputs, templates
    input_md = (args.input_md if os.path.isabs(args.input_md)
                else os.path.join(os.getcwd(), args.input_md))
    if not os.path.exists(input_md):
        print_error(f'Input file does not exist: {args.input_md}')
        exit(-1)

    input_dir = os.path.dirname(input_md)
    input_basename = os.path.splitext(os.path.basename(input_md))[0]

    template_dir = (args.template_dir if os.path.isabs(args.template_dir)
                    else os.path.join(os.getcwd(), args.template_dir))

    output_dir = (args.output_dir if os.path.isabs(args.output_dir)
                else os.path.join(os.getcwd(), args.output_dir))
    if os.path.exists(output_dir):
        print(Fore.BLUE + f"Using output directory: {output_dir}")
    else:
        print(Fore.BLUE + f"Creating output directory: {output_dir}")
        os.mkdir(output_dir)

    # Copy static images to output directory
    images_dir = os.path.join(os.getcwd(), args.images_dir)
    if os.path.exists(images_dir):
        print(Fore.BLUE +
            f"Copying images to output directory from: {args.images_dir}")
        output_images = os.path.join(output_dir, args.images_dir)
        if os.path.exists(output_images):
            shutil.rmtree(output_images)
        shutil.copytree(images_dir, output_images)

    # Copy other specified static files to output directory
    static_files = []
    for g in args.statics:
        path = g if os.path.isabs(g) else os.path.join(os.getcwd(), g)
        static_files += glob.glob(path, recursive=True)

    if len(static_files) > 0:
        print(Fore.BLUE +
            f"Copying static files to output directory:")
        for f in static_files:
            print(f"    {f}")
            if os.path.isdir(f):
                result_dir = os.path.join(output_dir, os.path.basename(f))
                if os.path.exists(result_dir):
                    shutil.rmtree(result_dir)
                shutil.copytree(f, result_dir)
            else:
                shutil.copy(f, output_dir)

    if build_md:
        # Build Markdown output
        output_file = os.path.join(output_dir, input_basename + '.md')
        print(Fore.BLUE + f"Building Markdown output: {output_file}")

        print(Fore.CYAN + f"Running pandoc")
        pandoc_params = [
            "pandoc",
            input_md,
            "--output", output_file,
            "--from", "markdown",
            "--filter", pandoc_pythonexec,
            "--filter", pandoc_crossref,
            "--filter", pandoc_citeproc,
            "-Mcref",
            "-Mlistings",
            f"-Mgithash={parse_git_branch()}{parse_git_hash()}"
        ]

        run_pandoc(pandoc_params, output_dir, verbose=args.verbose)

    if build_html:
        # Build HTML output
        output_file = os.path.join(output_dir, input_basename + '.html')
        print(Fore.BLUE + f"Building HTML output: {output_file}")
        template_file = find_template_file(template_dir, args.template, "html")
        if template_file is None:
            print(Fore.YELLOW +
                f"Did not find an HTML template in: {template_dir}")
        else:
            print(Fore.CYAN + f"Using template: {template_file}")

        # Look for SCSS or CSS style file in the template directory
        stylesheet_file = find_template_file(template_dir, args.template, 'scss')
        if stylesheet_file is not None:
            sass_exec = find_executable('sass', args.sass)
            infile = stylesheet_file
            stylesheet_file = os.path.join(
                output_dir,
                os.path.splitext(os.path.basename(infile))[0] + '.css')
            print(Fore.CYAN + f"Converting SCSS to CSS")
            subprocess.run([sass_exec,
                            infile,
                            stylesheet_file,
                            "--style",
                            "compressed"])
        else:
            stylesheet_file = find_template_file(template_dir,
                                                args.template,
                                                'css')
            if stylesheet_file:
                shutil.copy(stylesheet_file, output_dir)

        if stylesheet_file:
            stylesheet_file = os.path.basename(stylesheet_file)

        if template_dir:
            print(Fore.CYAN + f"Copying template files to output directory")
            template_files = glob.glob(os.path.join(template_dir, "*"))
            for f in template_files:
                if os.path.isfile(f):
                    shutil.copy(f, output_dir)

        print(Fore.CYAN + f"Running pandoc")
        pandoc_params = [
            "pandoc",
            input_md,
            "--output", output_file,
            "--from", "markdown",
            "--listings",
            "--toc",
            "--number-sections",
            "--filter", pandoc_pythonexec,
            "--filter", pandoc_crossref,
            "--filter", pandoc_citeproc,
            "--mathjax",
            "-Mcref",
            "-Mcolorlinks",
            "-MlinkReferences",
            "-Mlistings",
            "-Mlink-citations",
            f"-Mgithash={parse_git_branch()}{parse_git_hash()}"
        ]
        if template_file:
            pandoc_params.append('--template')
            pandoc_params.append(
                os.path.splitext(os.path.basename(template_file))[0])
        if stylesheet_file:
            pandoc_params.append(f'-Mcss={stylesheet_file}')
        if args.verbose:
            pandoc_params.append('--verbose')
        if args.self_contained:
            pandoc_params.append('--self-contained')

        run_pandoc(pandoc_params, output_dir, verbose=args.verbose)

    if build_pdf:
        # Build PDF output
        output_file = os.path.join(output_dir, input_basename + '.pdf')
        print(Fore.BLUE + f"Building PDF output: {output_file}")

        template_file = find_template_file(template_dir, args.template, "latex")
        if template_file is None:
            print(Fore.YELLOW +
                f"Did not find a LaTeX template in: {template_dir}")
        else:
            print(Fore.CYAN + f"Using template: {template_file}")

        if template_dir:
            print(Fore.CYAN + f"Copying template files to output directory")
            template_files = glob.glob(os.path.join(template_dir, "*"))
            for f in template_files:
                if os.path.isfile(f):
                    shutil.copy(f, output_dir)

        print(Fore.CYAN + f"Running pandoc")
        pandoc_params = [
            "pandoc",
            input_md,
            "--output", output_file,
            "--pdf-engine", "xelatex",
            "--from", "markdown",
            "--listings",
            "--toc",
            "--number-sections",
            "--filter", pandoc_pythonexec,
            "--filter", pandoc_crossref,
            "--filter", pandoc_citeproc,
            "-Mcref",
            "-Mcolorlinks",
            "-Mlistings",
            f"-Mgithash={parse_git_branch()}{parse_git_hash()}"
        ]
        if template_file:
            pandoc_params.append('--template')
            pandoc_params.append(
                os.path.splitext(os.path.basename(template_file))[0])
        if args.verbose:
            pandoc_params.append(f'--verbose')

        run_pandoc(pandoc_params, output_dir, verbose=args.verbose)

    print(Fore.GREEN + 'Complete')
    print(Style.RESET_ALL)