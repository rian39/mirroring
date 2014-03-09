# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd

# <codecell>

ops = pd.read_pickle('data/operations_results.pyd')

# <codecell>

ops_no_dups = ops_df.drop_duplicates(cols = ['publishedAt', 'videoId'])

# <codecell>

ops_no_dups = ops.drop_duplicates(cols = ['publishedAt', 'videoId'])

# <codecell>

ops = ops_no_dups

# <codecell>

# strip all the double spaces, and non-word characters 

# <codecell>

print(ops.title.str.lower().str.strip().str.replace('\\W+', ' ').value_counts()[:20])

# <codecell>

print('\n Videos with short titles\n')

# <codecell>

print(ops[(ops.title.apply(len) < 4)]['title'])

# <codecell>

ops['title_clean'] = ops.title.str.lower().str.strip().str.replace('\\W+', ' ')

# <codecell>

ops_pure = ops.ix[ops.title_clean.str.contains('anonymous operation')]

# <codecell>

%matplotlib

# <codecell>

titles = ops_pure.title_clean.value_counts()

# <codecell>

titles

# <codecell>

titles > 1

# <codecell>

titles[titles > 1]

# <codecell>

mirrors = titles[titles > 1]

# <codecell>

mirrors

# <codecell>

import matplotlib.pyplot as plt

# <codecell>

plt.figure(figsize=(10,4))

# <codecell>

plt.bar(mirrors)

# <codecell>

plt.bar?

# <codecell>

left = mirrors.index

# <codecell>

left

# <codecell>

range(0, len(mirrors))

# <codecell>

left = range(0, len(mirrors))

# <codecell>

heights = mirrors.values()

# <codecell>

heights = mirrors.values

# <codecell>

heights

# <codecell>

plt.bar(left, heights)

# <codecell>

plt.bar(left=left,height= heights)

# <codecell>

plt.xlabel('operation')

# <codecell>

plt.ylabel('mirror count')

# <codecell>

plt.bar?

# <codecell>

plt.bar?

# <codecell>

plt.bar(left=left,height= heights, width=0.1)

# <codecell>

plt.bar(left=left,height= heights, width=0.01)

# <codecell>

plt.bar(left=left,height= heights, width=0.01)

# <codecell>

history

# <codecell>

plt.barh(left=left,height= heights, width=0.01)

# <codecell>

plt.barh(left=left,height= heights)

# <codecell>

plt.barh(left,heights)

# <codecell>

%matplotlib?

# <codecell>

print(ops_pure.title_clean.unique())

# <codecell>

print(ops_pure.title_clean.unique()[:40])

# <codecell>

ops_pure.title_clean.unique()[:40]

# <codecell>

ops_pure.title_clean.str.strip().unique()[:40]

# <codecell>

t

# <codecell>

t = 'asdf'

# <codecell>

t.join?

# <codecell>

import datetime

# <codecell>

datetime

# <codecell>

datetime.time.strftime?

# <codecell>

ops

# <codecell>

ops.title

# <codecell>

ops.duration

# <codecell>

ops[['title', 'duration']
]

# <codecell>

ops[['title', 'duration']].map(lambda x,y: print(x,y))
]

# <codecell>

ops[['title', 'duration']].map(lambda x,y: print x)

# <codecell>

ops[['title', 'duration']].map(lambda x: print x)

# <codecell>

ops[['title', 'duration']]

# <codecell>

ops[['title', 'duration']].map(lambda x: x,y)

# <codecell>

ops.map(lambda x: x.title)

# <codecell>

ops.applymap?

# <codecell>

ops.apply?

# <codecell>

import YT_api_generate as yt

# <codecell>

ops = yt.format_durations(ops)

# <markdowncell>

# ## THIS THE KEY BIT TO LINK TITLES AND DURATIONS

# <codecell>

dur_ti = ops.groupby(ops.duration_time)['title'].value_counts()

# <codecell>

t=dt.time?

# <codecell>

t=dt.time(10,11,12)

# <codecell>

t.hour

# <codecell>

t.min

# <codecell>

t.minute

# <codecell>

t.second

# <codecell>

t.dst

# <codecell>

t.dst()

# <codecell>

t.strftime('HH::MM::SS')

# <codecell>

t.strftime('10::10::00')

# <codecell>

t.strftime?

# <codecell>

ops.duration_time

# <codecell>

ops.duration_time.apply(hour)

# <codecell>

ops.duration_time.apply(dt.hour)

# <codecell>

ops.duration_time.apply(dt.time.hour)

# <codecell>

ops.duration_time[0]

# <codecell>

ops.duration_time[:2]

# <codecell>

ops.duration_time[:1]

# <codecell>

t=ops.duration_time[:1]

# <codecell>

t

# <codecell>

import numpy as np

# <codecell>

t

# <codecell>

pd.datetools.Hour(t)

# <codecell>

t

# <codecell>

times=ops.duration_time

# <codecell>

times.median()

# <codecell>

times.max()

# <codecell>

times.mean()

# <codecell>

times.min()

# <codecell>

times[0].hour

# <codecell>

times[0]

# <codecell>

times.ix[0]

# <codecell>

ops.groupby(ops.duration_time)['title'].value_counts()

# <codecell>

ops.groupby(ops.duration_time)['title'].value_counts()[0]

# <codecell>

type(dur_ti)

# <codecell>

du_ti[0]

# <codecell>

dur_ti[0]

# <codecell>

dur_ti[:2]

# <codecell>

dur_ti[:4]

# <codecell>

dur_ti[:6]

# <codecell>

dur_ti.value_counts()

