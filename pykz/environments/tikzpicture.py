from .. import formatting
from ..tikzcode import TikzCode
from .. import environment as env
from . import axis as ax


class TikzPicture(env.Environment):

    def __init__(self, standalone: bool = True, **options):
        super().__init__("tikzpicture", **options)
        self.standalone = standalone
        self.preamble = TikzCode()

    def add_preamble_line(self, line: str):
        self.preamble.add_line(line)

    def add_axis(self, axis: ax.Axis):
        self.add(axis)
        self.preamble.usepackage("pgfplots")

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
        parent = os.path.dirname(filename)
        if parent:
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        if not filename.endswith(".tex") and \
           not filename.endswith(".tikz"):
            filename = filename + ".tex"

        with open(filename, "w") as f:
            f.write(self.get_code())

    def preview(self):
        from pykz.io import preview_latex_doc
        return preview_latex_doc(self.get_code())
