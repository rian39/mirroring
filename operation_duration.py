# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Anonynous operations in terms of how many videos comprise an operation and how they are mirrored

# <codecell>

%load_ext autoreload
%autoreload 2

# <codecell>

import YT_api_generate as yt
import pandas as pd
import re
import numpy as np
import ggplot
import matplotlib.pyplot as plt
import seaborn

# <codecell>

# raw search results from Youtube api
ops_df = pd.read_pickle('data/operations_results.pyd')

# <codecell>

ops = yt.title_clean_operations(ops_df)
ops = yt.format_durations(ops)
ops.shape

# <codecell>

print len(sort(ops.title_short.unique()))
sort(ops.title_short.unique())

# <codecell>

# calculate the duration of operations
# duration time is the length of a video used to find matches
end = ops.groupby(['title_short', 'duration_time']).publishedAt.max()
start = ops.groupby(['title_short', 'duration_time']).publishedAt.min()
operation_duration = end - start

# <codecell>

operation_duration[operation_duration>0]

# <codecell>

mirror_count = ops.groupby(['title_short', 'duration_time']).publishedAt.count()

# <codecell>

ops.groupby(['title_short', 'duration_time']).viewCount.max()
d = {'duration': operation_duration, 'mirror_count':mirror_count}
op_dur_count_df = pd.DataFrame(d)

# <codecell>

op_dur_count_df['start'] = start
op_dur_count_df['end'] = end

# <codecell>

op_dur_count_df.to_excel('data/operations_durations_count.xlsx')

# <codecell>

# only plot values where mirror > 1 
op_dur_count_df_plot = op_dur_count_df.ix[op_dur_count_df['mirror_count']>1]
op_dur_count_df_plot.sort(columns='start', inplace=True)
op_dur_count_df_plot.shape

# <markdowncell>

# # Plot the bar graph
# 
# I've cut the data down to rows that have more than 1 mirror.

# <codecell>

opnames = op_dur_count_df_plot.index.get_level_values(0).tolist()

# <codecell>

widt = op_dur_count_df_plot['duration'].map(lambda x: np.round(x/np.timedelta64(1, 'D'), decimals = 1)).tolist()
bot = range(0, len(opnames))
lef = op_dur_count_df_plot.start.tolist()
x_labs = pd.date_range(start = op_dur_count_df_plot['start'].min(), end =  op_dur_count_df_plot['end'].max(), freq = 'M')
f = plt.figure(figsize = (18,18))

# <codecell>

plt.barh(bot, widt, 0.2, lef)

# <codecell>

op_dur_count_df_plot[['duration', 'mirror_count', 'start']]

# <codecell>


