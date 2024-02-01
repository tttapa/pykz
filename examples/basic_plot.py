import numpy as np
import pykz

x = np.linspace(0, 10, 100)
y = np.sin(x)

pykz.plot(x, y)
pykz.preview()
# pykz.preview()
