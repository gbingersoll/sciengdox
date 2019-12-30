import mock
import pytest
from pytest_mock import mocker
import os

from sciengdox.figures import svg_figure
from svg import RootSvg


class FakeFig():
    def __init__(self, mocker):
        self.savefig = mocker.stub()


def setup_mocks(mocker, path_exists):
    mocker.patch('os.path.exists', return_value=path_exists)
    mocker.patch('os.makedirs')
    fig = FakeFig(mocker)
    return fig


def test_svg_figure_makes_default_output_directory_if_does_not_exist(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure')
    os.makedirs.assert_called_once_with('figures')


def test_svg_figure_does_not_makes_output_directory_if_it_not_exists(mocker):
    fig = setup_mocks(mocker, True)

    svg_figure(fig, 'myfigure')
    os.makedirs.assert_not_called()


def test_svg_figure_saves_the_figure_with_default_dirs(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure')
    fig.savefig.assert_called_once_with('figures/myfigure.svg',
                                        format='svg')


def test_svg_figure_returns_figure_url_with_default_dirs(mocker):
    fig = setup_mocks(mocker, False)

    url = svg_figure(fig, 'myfigure')
    assert(url) == 'figures/myfigure.svg'


def test_svg_figure_makes_specified_output_directory(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='outs')
    os.makedirs.assert_called_once_with('outs/figures')


def test_svg_figure_saves_the_figure_with_specified_output_dir(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='outs')
    fig.savefig.assert_called_once_with('outs/figures/myfigure.svg',
                                        format='svg')


def test_svg_figure_returns_figure_url_with_specified_output_dir(mocker):
    fig = setup_mocks(mocker, False)

    url = svg_figure(fig, 'myfigure', output_dir='outs')
    assert(url) == 'figures/myfigure.svg'


def test_svg_figure_makes_specified_figures_directory(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='output', figure_dir='figs')
    os.makedirs.assert_called_once_with('output/figs')


def test_svg_figure_saves_the_figure_with_specified_figures_dir(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='output', figure_dir='figs')
    fig.savefig.assert_called_once_with('output/figs/myfigure.svg',
                                        format='svg')


def test_svg_figure_returns_figure_url_with_specified_figures_dir(mocker):
    fig = setup_mocks(mocker, False)

    url = svg_figure(fig, 'myfigure', output_dir='outs', figure_dir='figs')
    assert(url) == 'figs/myfigure.svg'


def test_svg_figure_makes_directory_with_blank_figure_dir(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='output', figure_dir='')
    os.makedirs.assert_called_once_with('output')


def test_svg_figure_saves_the_figure_with_blank_figure_dir(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='output', figure_dir='')
    fig.savefig.assert_called_once_with('output/myfigure.svg', format='svg')


def test_svg_figure_returns_figure_url_with_blank_figure_dir(mocker):
    fig = setup_mocks(mocker, False)

    url = svg_figure(fig, 'myfigure', output_dir='outs', figure_dir='')
    assert(url) == 'myfigure.svg'


def test_svg_figure_handles_both_dir_args_blank(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='', figure_dir='')
    os.makedirs.assert_not_called()


def test_svg_figure_saves_the_figure_with_blank_output_and_fig_dirs(mocker):
    fig = setup_mocks(mocker, False)

    svg_figure(fig, 'myfigure', output_dir='', figure_dir='')
    fig.savefig.assert_called_once_with('myfigure.svg', format='svg')


def test_svg_figure_returns_figure_url_with_blank_output_and_fig_dirs(mocker):
    fig = setup_mocks(mocker, False)

    url = svg_figure(fig, 'myfigure', output_dir='', figure_dir='')
    assert(url) == 'myfigure.svg'


def test_svg_figure_saves_svg_diagram_to_correct_location(mocker):
    setup_mocks(mocker, True)
    fig = RootSvg((0, 1, 2, 3))
    fig.write = mocker.stub()

    url = svg_figure(fig, 'mysvgdiagram', figure_dir='figs', output_dir='outs')
    fig.write.assert_called_once_with('outs/figs/mysvgdiagram.svg')
    assert(url) == 'figs/mysvgdiagram.svg'
