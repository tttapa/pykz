"""
Low-level Tikz commands
========================

Use more low-level features of Tikz for added flexibility.
"""

import pykz

# %%
# Define your own styles

pykz.define_style("arrow", **{">": "stealth", "->": True})

pykz.line([(-1, 0), (1, 0)], arrow=True)
pykz.line([(0, -1), (0, 1)], arrow=True)
# pykz.preview()

# %%
# Alternatively, use the high-level functions

fig = pykz.figure()
fig.set_option(">", "stealth")
pykz.arrow([(-1, 0), (1, 0)])
pykz.arrow([(0, -1), (0, 1)])

# pykz.preview()
