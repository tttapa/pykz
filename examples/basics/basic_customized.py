"""Example showing some basic customization."""

import numpy as np
import pykz

x = np.linspace(0, 10, 100)
y = np.sin(x)
y2 = np.cos(x)

pykz.plot(x, y, color="black", label="sine function")
pykz.plot(x, y2, color="blue", label="cosine function")

pykz.preview()
