"""Public API"""

from .environments.axis import Axis
from .environments.tikzpicture import TikzPicture
from .commands.addplot import Addplot
from .commands.fillbetween import FillBetween
from .commands.node import Node
from .commands.draw import Draw
from .commands.circle import Circle
from .plot import create_plot
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
    WorkSpace.sca(None)
    WorkSpace.scf(pic)
    return pic


def ax(**options) -> Axis:
    ax = Axis(**options)
    fig = __get_or_create_fig()
    WorkSpace.sca(ax)
    fig.add_axis(ax)
    return ax


def dumps(fig: TikzPicture = None) -> str:
    """
    Dump the tex-code of the current figure to a string.

    If no figure is given, the active figure is selected,
    and the contents of this figure are returned.

    :param fig: Figure to codegen

    Returns
    -------
    str
    """
    fig = gcf() if fig is None else fig
    if fig is None:
        return ""
    return fig.get_code()


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


def save(filename: str, fig: TikzPicture = None, standalone: bool = False):
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
    fig.standalone = standalone
    return fig.export(filename)


def xlabel(lab: str):
    """Set the `y` label of the current axis.

    Arguments:
        - lab [str]: Label
    """
    ax = __get_or_create_ax()
    ax.set_xlabel(lab)


def xticks(ticks: np.ndarray, labels: list[str] = None, ax: Axis = None):
    """

    Set the x ticks and (optionally label them)

    Parameters
    ----------
    ticks
        x-coordinates to add ticks at
    labels
        Labels of the ticks
    ax
        The axis to modify. The current axes is used if None is passed.
    """
    ax = __get_or_create_ax() if ax is None else ax
    ax.set_xticks(ticks, labels)


def yticks(ticks: np.ndarray, labels: list[str] = None, ax: Axis = None):
    """

    Set the y ticks and (optionally label them)

    Parameters
    ----------
    ticks
        y-coordinates to add ticks at
    labels
        Labels of the ticks
    ax
        The axis to modify. The current axes is used if None is passed.
    """
    ax = __get_or_create_ax() if ax is None else ax
    ax.set_yticks(ticks, labels)


def zticks(ticks: np.ndarray, labels: list[str] = None, ax: Axis = None):
    """

    Set the z ticks and (optionally label them)

    Parameters
    ----------
    ticks
        z-coordinates to add ticks at
    labels
        Labels of the ticks
    ax
        The axis to modify. The current axes is used if None is passed.
    """
    ax = __get_or_create_ax() if ax is None else ax
    ax.set_zticks(ticks, labels)


def define_style(name: str, fig: TikzPicture = None, **options):
    fig = __get_or_create_fig() if fig is None else fig
    fig.set_style(name, **options)


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


def axhline(y: float, ax: Axis = None, **options) -> list[Addplot]:
    """Plot a horizontal line at the provided `y` value.
    """
    return plot(y, ax, **options)


def scale(scale: float, fig: TikzPicture = None):
    fig = gcf() if fig is None else fig
    fig.set_option("scale", scale)


def point(coordinates: np.ndarray = None,
          label: str = "",
          name: str = None,
          axis_coords: bool = None,
          label_loc: str = "above",
          size: int | str = "1pt",
          axis: Axis = None,
          fig: TikzPicture = None,
          **options) -> Node:
    """Draw a point at the given coordinates.

    It creates a node, but also adds some styling to make it look like a point.

    See also: [[node]].
    """
    options["pt"] = True
    nd = node(coordinates, label, name, axis_coords, label_loc, axis, fig, **options)
    fig = fig if fig is not None else __get_or_create_fig()
    fig.define_style("pt", inner_sep=size, circle=True, fill=True)
    return nd


def node(coordinates: np.ndarray = None,
         label: str = None,
         name: str = None,
         axis_coords: bool = None,
         label_loc: str = None,
         axis: Axis = None,
         fig: TikzPicture = None,
         **options) -> Node:
    """Draw a node at the given coordinates.

    Arguments:
        - coordinates: position of the point. Can be a numpy arraylike,
        or the name of a previously defined node. Caution: existence of this node
        is not checked! By default, no specific position is given, and Tikz handles it.
        - label: The label that is printed on the figure. By default,
        this label is printed inside the node.
        This can be changed by using the `label_loc` argument.
        - axis_coords:  Interpret the position in axis coordinates.
        If the coordinates are passed as a literal string, this option has no effect.
        - label_loc = "above" | "below" | "right" | "left" or a combination (starting with the vertical position),
        e.g., "above right". By default, it is None, and the label is added at the location of the node itself.
    """
    if axis_coords is None:
        given_axis = gca() if axis is None else axis
        axis_coords = False if given_axis is None else True

    if not label:
        label_loc = None
    node = Node(label, name, coordinates, label_loc, axis_coords, **options)
    if axis is None and axis_coords:
        axis = __get_or_create_ax()
        axis.add(node)
        return node

    fig = fig if fig is not None else __get_or_create_fig()
    fig.add(node)
    return node


def fill_between(x: np.ndarray, y1: np.ndarray, y2: np.ndarray, *,
                 draw_options=None, fill_options=None) -> FillBetween:
    """Fill the area between y1 and y2."""
    ax = __get_or_create_ax()
    ax.add_requirement(r"\usepgfplotslibrary{fillbetween}")

    draw_options = draw_options if draw_options is not None else dict()
    fill_options = fill_options if fill_options is not None else dict()

    draw_options["name path"] = "first"
    plot(x, y1, ax, **draw_options)

    draw_options["name path"] = "second"
    plot(x, y2, ax, **draw_options)[0]

    fill_plot = FillBetween("first", "second", **fill_options)
    ax.add(fill_plot)
    return fill_plot


# def quiver(x: np.ndarray, y: np.ndarray, dx: np.ndarray, dy: np.ndarray, **options) -> Quiver


def axvline(x: float, ax: Axis = None, **options) -> list[Addplot]:
    """Plot a vertical line at the provided `x` value."""
    # TODO: Think of ways to represent this allow axes dimensions to be updated afterwards.
    ax = ax if ax is not None else __get_or_create_ax()
    ymin, ymax = ax.get_ylims()
    xes = np.array((x, x))
    ys = np.array((ymin, ymax))
    return plot(xes, ys, ax=ax, **options)


Point = np.ndarray | str | Node


def __create_draw(connector_type: str, points: list[Point], **options) -> Draw:
    from pykz.commands import Connector
    connector = Connector(connector_type)
    draw = Draw(points, connector, **options)
    return draw


def __add_draw_command(draw: Draw) -> Draw:
    fig = __get_or_create_fig()
    fig.add(draw)
    return draw


def __create_and_add_draw(connector_type: str, points: list[Point], **options):
    draw = __create_draw(connector_type, points, **options)
    return __add_draw_command(draw)


def rectangle(c1: Point, c2: Point, **options) -> Draw:
    return __create_and_add_draw("rectangle", [c1, c2], **options)


def circle(center: Point, radius: float, **options) -> Circle:
    circle = Circle(center, radius, **options)
    return __add_draw_command(circle)


def line(points: list[Point], connection: str = "--", **options) -> Draw:
    return __create_and_add_draw(connection, points, **options)


def arrow(points: list[Point], forward: bool = True, backward: bool = False,
          arrowhead: str = None, **options) -> Draw:
    bw = "<" if backward else ""
    fw = ">" if forward else ""
    arrow = bw + "-" + fw if (bw or fw) else "--"
    arrow_opts = {arrow: True}
    if arrowhead is not None:
        if forward:
            arrow_opts[">"] = arrowhead
        if backward:
            arrow_opts["<"] = arrowhead
    options.update(arrow_opts)
    return line(points, **options)


def plot(x, y=None, z=None, ax: Axis = None, label: str | tuple[str] = None,
         inline_label: bool = False,
         **options) -> list[Addplot]:

    ax = ax if ax is not None else __get_or_create_ax()
    plot_commands = create_plot(x, y, z, label, inline_label, **options)
    for plt in plot_commands:
        ax.add(plt)
    return plot_commands


def scatter(x, y=None, z=None, ax: Axis = None, label: str | tuple[str] = None,
            inline_label: bool = False,
            **options) -> list[Addplot]:
    options["only marks"] = True
    return plot(x, y, z, ax, label, inline_label, **options)

