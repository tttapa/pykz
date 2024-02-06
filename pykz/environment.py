from dataclasses import dataclass
from .tikzcode import TikzCode, Tex
from .options import Options
from typing import Union
from .formatting import wrap_env


@dataclass
class Environment(Tex):
    """Representation of a LaTeX environment."""

    def __init__(self, name: str, **options):
        self.name = name
        self.options = Options(**options)
        self.content = TikzCode()

    def add(self, content: Union[Tex, str]):
        self.content.add_line(content)

    def get_code(self) -> str:
        return wrap_env(self.name, self.content.get_code(), **self.options)

    def set_option(self, name: str, value: str):
        self.options.set_option(name, value)

    def update_option(self, name: str, inner_key: str, value: str):
        suboption = self.options.get(name, Options())
        if not isinstance(suboption, Options):
            raise TypeError(f"Cannot update sub-options. Option {suboption} is a string.")
        suboption.set_option(inner_key, value)
        self.options[name] = suboption

    def set_options(self, **options):
        self.options.set_options(**options)
