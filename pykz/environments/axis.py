from dataclasses import dataclass
from enum import Enum
from ..environment import Environment


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


class Axis(Environment):

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
