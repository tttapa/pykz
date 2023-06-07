from dataclasses import dataclass
from .tikzcode import TikzCode
from typing import Union
from formatting import wrap_env


@dataclass
class Environment:
    """Representation of a LaTeX environment."""

    def __init__(self, name: str, **options):
        self.name = name
        self.options = {name.replace("_", " "): value for name, value in options.items()}
        self.content = TikzCode()

    def add(self, content: Union['Environment', str]):
        if isinstance(content, Environment):
            content = content.get_code()
        self.content.add_line(content)

    def get_code(self) -> str:
        return wrap_env(self.name, self.content.get_code(), **self.options)
