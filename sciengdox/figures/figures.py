import os
from svg import RootSvg


def svg_figure(fig,
               basename,
               figure_dir='figures',
               output_dir=''):
    if output_dir == '':
        output_dir = figure_dir
    elif figure_dir != '':
        output_dir = '/'.join([output_dir, figure_dir])

    if output_dir != '' and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f'{basename}.svg'
    output_file = f'{output_dir}/{filename}' if output_dir != '' else filename

    if isinstance(fig, RootSvg):
        fig.write(output_file)
    else:
        fig.savefig(output_file, format='svg')

    file_url = f'{figure_dir}/{filename}' if figure_dir != '' else filename
    return file_url
