from dataclasses import dataclass
from enum import Enum
from .. import environment as env


@dataclass
class View:
    azimuth: int
    elevation: int

    def __str__(self) -> str:
        return f"{{{self.azimuth}}}{{{self.elevation}}}"


class AxisMode(Enum):
    normal = "normal"
    linear = "linear"
    log = "log"


class AxisDir(Enum):
    normal = "normal"
    reverse = "reverse"


class Grid(Enum):
    minor = "minor"
    major = "major"
    both = "both"
    none = "none"


class Axis(env.Environment):

    def __init__(self,
                 xlabel: str = None,
                 ylabel: str = None,
                 view: View = None,
                 width: str = None,
                 height: str = None,
                 scale_only_axis: bool = False,
                 axis_x_line: str = None,
                 axis_y_line: str = None,
                 axis_z_line: str = None,
                 xmode: AxisMode = None,
                 ymode: AxisMode = None,
                 zmode: AxisMode = None,
                 x_dir: AxisDir = None,
                 y_dir: AxisDir = None,
                 z_dir: AxisDir = None,
                 axis_equal: bool = False,
                 axis_equal_image: bool = False,
                 xmin: float = None, xmax: float = None,
                 ymin: float = None, ymax: float = None,
                 zmin: float = None, zmax: float = None,
                 grid: Grid = None,
                 xminorgrids: bool = None,
                 yminorgrids: bool = None,
                 zminorgrids: bool = None,
                 xmajorgrids: bool = None,
                 ymajorgrids: bool = None,
                 zmajorgrids: bool = None,
                 xtick: str = None,
                 ytick: str = None,
                 ztick: str = None,
                 **extra
                 ):
        arguments = locals()
        arguments.pop("extra")
        arguments.pop("self")
        arguments.pop("__class__")
        arguments = {key.replace("_", " "): value for (key, value) in arguments.items()
                     if value is not None
                     }
        super().__init__("axis", **arguments, **extra)

    def set_xlabel(self, label: str):
        self.options.set_option("xlabel", label)

    def set_ylabel(self, label: str):
        self.options.set_option("ylabel", label)

    def set_zlabel(self, label: str):
        self.options.set_option("zlabel", label)

    def set_xlims(self, lims: tuple[float]):
        (self.options["xmin"], self.options["xmax"]) = lims

    def set_ylims(self, lims: tuple[float]):
        (self.options["ymin"], self.options["ymax"]) = lims

    def set_zlims(self, lims: tuple[float]):
        (self.options["zmin"], self.options["zmax"]) = lims

    def set_xmax(self, v):
        self.options["xmax"] = v

    def set_ymax(self, v):
        self.options["ymax"] = v

    def set_zmax(self, v):
        self.options["zmax"] = v

    def set_xmin(self, v):
        self.options["xmin"] = v

    def set_ymin(self, v):
        self.options["ymin"] = v

    def set_zmin(self, v):
        self.options["zmin"] = v

