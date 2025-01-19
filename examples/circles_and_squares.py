"""
Directly using Tikz
=====================

Directly use Tikz functionality, without pgfplots.
"""

import pykz


rect = pykz.rectangle((-1, -1), (1, 1))
circle = pykz.circle((2, 0), (1), fill="red")

rect2 = pykz.rectangle((1, 1), (2, 3), fill="cyan")

# Dump the generated tikz code to the stdout.
print(pykz.dumps())

pykz.save("circles.tex", standalone=True)

# Save the Tikz code to a temporary file, compile it, and open the pdf in the default viewer.
# pykz.preview()
