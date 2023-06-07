from . import formatting
from ..tikzcode import TikzCode
from ..environment import Environment


class TikzPicture(Environment):

    def __init__(self, standalone: bool = True, **options):
        super().__init__("tikzpicture", **options)
        self.standalone = standalone
        self.preamble = TikzCode()

    def add_preamble_line(self, line: str):
        self.preamble.add_line(line)

    def get_code(self) -> str:
        preamble = ""
        if self.standalone:
            preamble += "\\documentclass[tikz]{standalone}\n"
            preamble += self.preamble.get_code()
        else:
            preamble = ""

        content = self.content.get_code()
        content = formatting.wrap_env("tikzpicture", content)
        if self.standalone:
            content = formatting.wrap_env("document", content)

        return preamble + content

    def export(self, filename: str):

        # Create the file directory if it doesn't exist already.
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w") as f:
            f.write(self.get_code())

    def preview(self):
        from pykz.io import preview_latex_doc
        return preview_latex_doc(self.get_code())
