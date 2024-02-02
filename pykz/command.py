from .tikzcode import Tex
from .options import Options


class Command(Tex):
    r"""A LaTeX Command of the form `\cmdname[options]{arg1}{arg2}`."""

    def __init__(self, cmd: str, *arguments, **options):
        self.cmd_name: str = cmd
        self._options: Options = Options(**options)
        self._arguments: list[Tex] = []
        for argument in arguments:
            self.add_argument(argument)

    def add_argument(self, argument: str | Tex):
        if isinstance(argument, str):
            argument = Tex(argument)
        self._arguments.append(argument)

    def get_code(self) -> str:
        options_str = self._options.format()
        argument_str = ""
        for argument in self._arguments:
            argument_str += f"{{{argument.get_code()}}}"

        return f"\\{self.cmd_name}{options_str}{argument_str}"

    def set_option(self, key: str, value: str):
        self._options.set_option(key, value)

    def set_options(self, **opts):
        self._options.set_options(**opts)
