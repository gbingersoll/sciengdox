import os
import pathlib
from svg import RootSvg

try:
    import matplotlib.figure
    matplotlib_loaded = True
except ModuleNotFoundError:
    matplotlib_loaded = False

try:
    import plotly  # noqa: F401
    import plotly.io
    plotly_loaded = True
except ModuleNotFoundError:
    plotly_loaded = False


def svg_figure(fig, basename, figure_dir="figures", output_dir="", interactive=False):
    if output_dir == "":
        output_dir = pathlib.Path(figure_dir)
    elif figure_dir != "":
        output_dir = pathlib.Path(output_dir) / figure_dir
    else:
        output_dir = pathlib.Path(output_dir)

    if not output_dir.exists():
        os.makedirs(output_dir)

    filename = f"{basename}.svg"
    output_file = f"{output_dir}/{filename}" if output_dir != "" else filename

    if isinstance(fig, RootSvg):
        fig.write(output_file)
    elif matplotlib_loaded and isinstance(fig, matplotlib.figure.Figure):
        fig.savefig(output_file, format="svg")
    elif plotly_loaded and str(type(fig).__module__).find("plotly") != -1:
        if interactive:
            return plotly.io.to_html(fig, include_plotlyjs=False, full_html=False)
        fig.write_image(output_file)  # Note: requires 'kaleido' package
    else:
        raise Exception(
            "Unknown figure type.  Try installing matplotlib or plotly.")

    file_url = f"{figure_dir}/{filename}" if figure_dir != "" else filename
    return file_url
