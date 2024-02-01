import numpy as np


def format_options(**options) -> str:
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

    return f"\\begin{{{envname}}}{format_options(**options)}\n{wrapped}\n\\end{{{envname}}}"


def format_vector(vector: np.ndarray,
                  separator: str = " ",
                  ints: bool = False) -> str:
    """Format a vector as a string by joining it with the provided separator."""
    if ints:
        formatted = [f"{int(element):d}" for element in vector]
    else:
        formatted = [f"{element:2.9f}" for element in vector]
    return separator.join(formatted)


def format_matrix(matrix: np.ndarray) -> str:
    """Format a matrix for use in an \\addplot command.

    Args:
        matrix (np.ndarray): data

    Returns:
        str: Formatted table
    """
    if np.ndim(matrix) == 0:
        return f"{float(matrix):2.16f}"
    if np.ndim(matrix) == 1:
        return format_vector(matrix)
    elif np.ndim(matrix) == 2:
        return '\n'.join([format_vector(row) for row in matrix])
    else:
        raise ValueError(f"Plotting {np.ndim(matrix)}-dimensional data is not supported.")
