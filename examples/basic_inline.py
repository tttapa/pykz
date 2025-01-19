"""
Minimal working example
=========================
Minimal working example of `pykz`, plotting a simple sine function.
"""

import numpy as np
import pykz

x = np.linspace(0, 10, 100)
y = np.sin(x)

pykz.plot(x, y)

# (Optional) save the tikz code to a file.
pykz.save("basic_inline.tex", standalone=True)
pykz.io.build_latex_file("basic_inline.tex")

# Save the Tikz code to a temporary file, compile it, and open the pdf in the default viewer.
# pykz.preview()
