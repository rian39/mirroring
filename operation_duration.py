# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Trying out Youtube downloads

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

# <markdowncell>

# ## Plotting the operations in terms of how many videos comprise an operation and how they are mirrored

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

import YT_api_generate as yt
import pandas as pd
import re
import numpy as np

# <codecell>

ops = pd.read_pickle('data/operations_results.pyd')

# <codecell>

ops = yt.title_clean_operations(ops)
ops = yt.format_durations(ops)

# <codecell>

ops.shape

# <codecell>

end = ops.groupby(['title_short', 'duration_time']).publishedAt.max()

# <codecell>

start = ops.groupby(['title_short', 'duration_time']).publishedAt.min()

# <codecell>

operation_duration = end - start

# <codecell>

operation_duration[operation_duration>0]

# <codecell>

mirror_count = ops.groupby(['title_short', 'duration_time']).publishedAt.count()

# <codecell>

ops.groupby(['title_short', 'duration_time']).viewCount.max()

# <codecell>

d = {'duration': operation_duration, 'mirror_count':mirror_count}

# <codecell>

op_dur_count_df = pd.DataFrame(d)

# <codecell>

op_dur_count_df['start'] = start

# <codecell>

op_dur_count_df.to_excel('data/operations_durations_count.xlsx')

# <codecell>

op_dur_count_df.index.get_level_values

# <codecell>

# only plot values where mirror > 1 
op_dur_count_df_plot = op_dur_count_df.ix[op_dur_count_df['mirror_count']>1]
op_dur_count_df_plot.sort(columns='start', inplace=True)
op_dur_count_df_plot.shape

# <markdowncell>

# # Plot the bar graph
# 
# I've cut the data down to rows that have more than 1 mirror. This reduces from around 1000 to 350.

# <codecell>

opnames = op_dur_count_df_plot.index.get_level_values(0).tolist()

# <codecell>

widt = op_dur_count_df_plot['duration'].map(lambda x: np.round(x/np.timedelta64(1, 'D'), decimals = 1)).tolist()

# <codecell>

bot = range(0, len(opnames))
lef = op_dur_count_df_plot.start.tolist()

# <codecell>

x_labs = pd.date_range(start = start.min(), end = end.max(), freq = 'M')

# <codecell>

%matplotlib 
import matplotlib.pyplot as plt
import seaborn

# <codecell>

f = plt.figure(figsize = (14,10))

# <codecell>

plt.barh(bot, widt, 0.2, lef)

# <codecell>

op_dur_count_df_plot[['duration', 'mirror_count', 'start']]

# <codecell>


