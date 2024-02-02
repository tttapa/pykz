"""Minimal working example of `pykz`, plotting a simple sine function."""

import numpy as np
import pykz

x = np.linspace(0, 10, 100)
y = np.sin(x)

pykz.plot(x, y)

# (Optional) save the tikz code to a file.
pykz.save("test-basic-plot.tex")

# Save the Tikz code to a temporary file, compile it, and open the pdf in the default viewer.
pykz.preview()
