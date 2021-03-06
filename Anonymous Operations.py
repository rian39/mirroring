# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

import pandas as pd
import YT_api_generate as yt
from pylab import *
import seaborn
import re
from IPython.display import HTML
from IPython.display import YouTubeVideo
pd.set_option("display.max_columns", 6)
pd.set_option("display.max_rows", 15)
pd.set_option("display.notebook_repr_html", True)
from optparse import OptionParser

# <codecell>

operations = [op.replace('\n', '') for op in open('data/query list').readlines()]

# <codecell>

operations

# <codecell>

df_ops = pd.DataFrame()
for op in operations:
    df  = yt.youtube_search(op,1000, True)
    df['operation'] = op
    df_ops = df_ops.append(df)

# <codecell>

df  = yt.youtube_search(operations[-1],1000, True)
df['operation'] = operations[-1]
df_ops = df_ops.append(df)

# <codecell>

print ('overall video details:' + str(df_ops.shape))

# <codecell>

# local save  -- around 25Mb
df_ops.to_pickle('data/operations_results.pyd')

# <codecell>

df1.description.ix[df1.viewCount.idxmax()]

# <codecell>

df1.title.value_counts()

# <markdowncell>

# List of titles shows that data still needs cleaning. How to clean out all these none-anonymous videos?

