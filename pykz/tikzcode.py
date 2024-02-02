from typing import Union
from . import formatting


class Tex:

    def __init__(self, code: str):
        self.code = code

    def __str__(self) -> str:
        self.get_code()

    def get_code(self) -> str:
        return self.code


class TikzCode:
    """Low-level representation of tikz code.
    The tikz code is represented as a list of lines.
    The methods of this function can be used to easily add new
    lines to the tikz code.
    """

    def __str__(self) -> str:
        return self.get_code()

    def __repr__(self) -> str:
        return f"{self.__class__}\n{self.get_code()}"

    def __init__(self):
        self.lines = []

    def __cmd(self, cmd: str) -> "TikzCode":
        self.add_line(Tex(cmd))
        return self

    def colorlet(self, colorname: str, colordef: str) -> "TikzCode":
        """Define a new color using the ``\\colorlet`` command of xcolor."""
        return self.__cmd(f"\\colorlet{{{colorname}}}{{{colordef}}}")

    def usepackage(self, package: str, **options) -> "TikzCode":
        return self.__cmd(f"\\usepackage{formatting.format_options(**options)}{{{package}}}")

    def node(self,
             label_text: str, name: str = "", location: Union[tuple, str] = "",
             **options) -> "TikzCode":
        location_str = f"at {location}" if location else ""
        return self.__cmd(f"\\node{formatting.format_options(**options)} ({name}) {location_str} {{{label_text}}};")

    def coordinate(self, name: str = "", location: Union[tuple, str] = "", **options) -> "TikzCode":
        location_str = f"at {location}" if location else ""
        return self.__cmd(f"\\coordinate{formatting.format_options(**options)} ({name}) {location_str};")

    def draw(self, *coordinates, **options) -> "TikzCode":
        return self.__cmd(f"\\draw{formatting.format_options(**options)} {'--'.join(coordinates)};")

    def add_line(self, line: Tex | str) -> "TikzCode":
        if isinstance(line, str):
            line = Tex(line)
        self.lines.append(line)

    def get_code(self) -> str:
        return "\n".join(line.get_code() for line in self.lines) + "\n"
