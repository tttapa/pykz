
def formatting.format_options(**options) -> str:
    """Convert the given dictionary of options to a string of options for
    a LaTeX environment.
    """
    opts = []
    for name, value in options.items():
        if isinstance(value, bool):
            if value:
                opts.append(str(name))
        else:
            opts.append(f"{name}={value}")

    if opts:
        options_str = ',\n'.join(opts)
        return f"[{options_str}]"
    return ""


def wrap_env(envname: str, wrapped: str, **options) -> str:
    r"""Wrap the ``wrapped`` string into a LaTeX environment with the name ``envname``.
    The dictionary of options represent options for the LaTeX environment.

    Example:

        ```
        wrap_env("axis", r"\addplot", width=4)
        ```
        generates
        ```
        \begin{axis}[width=4]
            \addplot
        \end{axis}
        ```
    """

    return f"\\begin{{{envname}}}{formatting.format_options(**options)}\n{wrapped}\n\\end{{{envname}}}"
