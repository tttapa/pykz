import numpy as np
from .formatting import format_matrix


def get_plot_command(
        data: np.ndarray,
        raw_options: str = "",
        suffix: str = "",
        plot3d: bool = False,
        plotplus: bool = False,
        label: str = None,
        inline_label: bool = False,
        labelopts: str = "") -> str:
    """Return a plot command to plot the given data in pgfplots.
    """
    labelcmd = ""
    if label:
        if inline_label:
            suffix += f"\\node[{labelopts}] {label}"
        else:
            labelcmd = f"\\addlegendentry{{{label}}}"
    tablecmd = "table" if np.ndim(data) >= 1 else ""
    return f"""
\\addplot{'3' if plot3d else ''}{'+' if plotplus else ''}[{raw_options}]
{tablecmd}{{%
{format_matrix(data)}
}}{suffix};
{labelcmd}
"""
