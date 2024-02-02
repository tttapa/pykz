from .environments.tikzpicture import TikzPicture
from .environments.axis import Axis
from .commands.addplot import Addplot
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


def __get_or_create_ax() -> Axis:
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
    """Preview the current figure.

    If no figure is given, the active figure is selected.
    The contents of this figure are written to a temporary file,
    compiled to a pdf and then opened in the default viewer.
    After the process terminates, these files are removed.

    Arguments:
        - fig [TikzPicture]: The Tikzpicture to preview.
    """
    fig = gcf() if fig is None else fig
    if fig is None:
        return
    fig.preview()


def save(filename: str, fig: TikzPicture = None):
    """Save the generated Tikz code to a file.

    If no figure is given, the active figure is selected.
    The contents of this figure are written to the given file.

    Arguments:
        - filename [str]: The path to write the figure to.
        If the extension `.tex` or `.tikz` is not present, `.tex` is appended to the filename.
        - fig [TikzPicture]: The Tikzpicture to preview.
    """

    fig = gcf() if fig is None else fig
    if fig is None:
        return
    return fig.export(filename)


def xlabel(lab: str):
    """Set the `y` label of the current axis.

    Arguments:
        - lab [str]: Label
    """
    ax = __get_or_create_ax()
    ax.set_xlabel(lab)


def ylabel(lab: str):
    """Set the `y` label of the current axis.

    Arguments:
        - lab [str]: Label
    """
    ax = __get_or_create_ax()
    ax.set_ylabel(lab)


def zlabel(lab: str):
    """Set the `z` label of the current axis.

    Arguments:
        - lab [str]: Label
    """
    ax = __get_or_create_ax()
    ax.set_zlabel(lab)


def xlim(limits: tuple[float]):
    """Set the `x` limits of the current axis.

    Arguments:
        - limits [tuple[float]]: Label
    """
    ax = __get_or_create_ax()
    ax.set_xlims(limits)


def ylim(limits: tuple[float]):
    """Set the `y` limits of the current axis.

    Arguments:
        - limits [tuple[float]]: Label
    """
    ax = __get_or_create_ax()
    ax.set_ylims(limits)


def plot(x, y=None, ax: Axis = None, label: str | tuple[str] = None,
         inline_label: bool = False,
         **options) -> Addplot:

    ax = ax if ax is not None else __get_or_create_ax()

    if y is None:  # Plot index vs. x
        datasets = (
            np.hstack((np.arange(len(row))[:, np.newaxis],
                       row[:, np.newaxis]))
            for row in x
        )
    else:
        datasets = (
            np.hstack((x_row[:, np.newaxis], y_row[:, np.newaxis]))
            for x_row, y_row in zip(np.atleast_2d(x), np.atleast_2d(y))
        )

    def iter_label():
        if label is None:
            yield None
        elif isinstance(label, str):
            while True:
                yield label
        else:
            for lab in label:
                yield lab
            yield None

    plot_commands = [Addplot(dataset, lab, inline_label=inline_label, **options) for lab, dataset in zip(iter_label(), datasets)]
    for plt in plot_commands:
        ax.add(plt)
    return plot_commands
