# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Trying out Youtube downloads
# 
# Can download videos and look at their attributes

# <codecell>

import pafy

# <codecell>

vid = pafy.Pafy('TOgk9WW1Q8c')

# <codecell>

vid.length

# <codecell>

vid.published

# <codecell>

vid.streams

# <codecell>

vid.expiry

# <codecell>

vid.description

# <codecell>

best = vid.getbest()

# <codecell>

best.download('images/test.mp4')

