from .environments.tikzpicture import TikzPicture
from .environments.axis import Axis
import numpy as np
from typing import Optional


class WorkSpace:
    __currfig = None
    __currax = None

    @classmethod
    def scf(cls, fig: TikzPicture):
        cls.__currfig = fig

    @classmethod
    def sca(cls, ax: TikzPicture):
        cls.__currax = ax

    @classmethod
    def gcf(cls) -> Optional[Axis]:
        return cls.__currfig

    @classmethod
    def gca(cls) -> Optional[Axis]:
        return cls.__currax


def gcf() -> Optional[TikzPicture]:
    return WorkSpace.gcf()


def gca() -> Optional[Axis]:
    return WorkSpace.gca()


def __get_or_create_fig() -> TikzPicture:
    f = gcf()
    return f if f is not None else figure()


def __get_or_create_ax() -> TikzPicture:
    a = gca()
    return a if a is not None else ax()


def figure(standalone: bool = True, **options) -> TikzPicture:
    pic = TikzPicture(standalone, **options)
    WorkSpace.scf(pic)
    return pic


def ax() -> Axis:
    ax = Axis()
    fig = __get_or_create_fig()
    WorkSpace.sca(ax)
    fig.add_axis(ax)
    return ax


def preview(fig: TikzPicture = None):
    fig = gcf() if fig is None else fig
    if fig is None:
        return
    fig.preview()


def save(filename: str, fig: TikzPicture = None):
    fig = gcf() if fig is None else fig
    if fig is None:
        return
    return fig.export(filename)


def plot(x, y=None, ax: Axis = None) -> Axis:
    from .plot import get_plot_command

    ax = ax if ax is not None else __get_or_create_ax()

    if y is None:
        plot_commands = (
            get_plot_command(
                np.hstack((np.arange(len(row))[:, np.newaxis],
                           row[:, np.newaxis]))
            )
            for row in np.atleast_2d(x)
        )
    else:
        plot_commands = (
            get_plot_command(
                np.hstack((x_row[:, np.newaxis], y_row[:, np.newaxis]))
            )
            for x_row, y_row in zip(np.atleast_2d(x), np.atleast_2d(y))
        )

    for plt in plot_commands:
        ax.add(plt)
    return ax
