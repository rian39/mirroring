# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext autoreload
%autoreload 2
%matplotlib inline

# <codecell>

import pandas as pd
import YT_api_generate as yt
import seaborn
import re
from optparse import OptionParser
from IPython.display import HTML
from IPython.display import YouTubeVideo
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", 6)
pd.set_option("display.max_rows", 15)
pd.set_option("display.notebook_repr_html", True)

# <markdowncell>

# # Mirroring and Anonymous
# 
# We are trying to gain an empirical sense of the extent and shape of mirroring practices in the Anonymous movement. We are focusing on Youtube video mirroring (why? Adam). 
# There are various problems in trying to get a sense of mirroring practice on Youtube. [TBA -- a description of this]
# 
# ## What we'd like to produce:
# 
# 1. A quantitative description of how many mirrored videos exist, when they were published and on what topics
# 2. A timeline of mirroring events associated with Anonymous. The timeline should describe their relative importance
# 
# 
# ## The list of Anonymous operations
# 
# Youtube searches using the API only return 500 results. (I guess most people don't want to look at more than a couple of pages of results). But a given operation might have 700 or 2400 mirrors. It is hard to get around this.
# Our main strategy has been to use _operations_ to multiply our search queries. We have found around 80 Anonymous operations. We run Youtube queries on all of these. We also run another set of 80 queries with the word 'mirror' added to the operation. The idea here is that we are creating a large query out of many smaller queries tiled together. 

# <codecell>

# felipe produced a list of operations
operations = [op.replace('\n', '') for op in open('data/operations_list.txt').readlines()]
operations_mirror = [op + ' mirror' for op in operations]

# <codecell>

operations.sort()
operations

# <codecell>

df_ops = pd.DataFrame()

# <codecell>

## the basic operations

for op in operations:
    df  = yt.youtube_search(op,1000, True)
    df['operation'] = op
    df_ops = df_ops.append(df)

# <markdowncell>

# Run all the same queries with 'mirror' as well. This might help address the unpredictability of the Youtube search results and its 'denial of search results'. So, we undertake a 'supply of service' approach here. 

# <codecell>

## run the same operations with 'mirror'



for op in operations_mirror:
    df  = yt.youtube_search(op,1000, True)
    df['operation'] = op
    df_ops = df_ops.append(df)

# <codecell>

df  = yt.youtube_search(operations[-1],1000, True)
df['operation'] = operations[-1]
df_ops = df_ops.append(df)

# <codecell>

df  = yt.youtube_search(operations_mirror[-1],1000, True)
df['operation'] = operations_mirror[-1]
df_ops = df_ops.append(df)

# <codecell>

print ('overall video details:' + str(df_ops.shape))

# <markdowncell>

# ## Save and read data for offline use
# 
# Don't want to run the queries every time, so saving them locally. 

# <codecell>

# local save  -- around 25Mb
df_ops.to_pickle('data/operations_results.pyd')

# <codecell>

ops_df = pd.read_pickle('data/operations_results.pyd')

# <codecell>

print('Dataset has %d rows'% ops_df.shape[0])

# <markdowncell>

# ## Dealing with the duplicates and finding mirrors in Youtube search results
# 
# We have run searches on Youtube that yield many results. But given that we are trying to look at 'mirroring,' how do we know whether a given result is a _duplicate_ produced by our overlapping search queries or an actual _mirror_? We need to get ride of duplicate search query results and then identify mirror results

# <codecell>

ops_df.columns

# <markdowncell>

# The columns that separate duplicates are
# 
# 1. publishedAt
# 2. videoId
# 
# If two results are published at the same time, and have the same videoID, we assume they are duplicates. We can drop these from the dataset. 
# n.b. If Youtube itself aggregates mirrored copies to a single videoID as part of its content management, we have a slight problem. But presumably the publication dates of mirrors would still be different. 

# <codecell>

ops_no_dups = ops_df.drop_duplicates(cols = ['publishedAt', 'videoId'])
print('None duplicated results: %d' % ops_no_dups.shape[0])

# <codecell>

ops_no_dups.head()

# <markdowncell>

# ## Identifying mirrors
# 
# This leaves a dataset that has no duplicateresults (i.e rows). Finding mirrored videos is potentially harder. Trying to think this through:
# 
# 1. If durations are the same and the titles overlap, we probably have a mirror. The practical problem here is finding the overlapping titles. Slightly different wordings for titles will be hard to track. And what about people who completely drop the titles when they mirror? This requires some slightly clever matching. 
# 2. Conversely, distinguish videos that have the same title but are different videos. They will have different durations. Obviously descriptions, number of comments, etc, are likely to be different.
# 3. decide which of the remain videos are Anonymous operations as opposed to media coverage, commentaries, reports, attacks, etc on Anonymous operations

# <markdowncell>

# ### Using titles to find duplicates

# <codecell>

# this shows some of the problems
ops = ops_no_dups

# strip all the double spaces, and non-word characters 
print(ops.title.str.lower().str.strip().str.replace('\\W+', ' ').value_counts()[:20])
print('\n Videos with short titles\n')
print(ops[(ops.title.apply(len) < 4)]['title'])

ops['title_clean'] = ops.title.str.lower().str.replace('\\W+', ' ').str.strip()

# <markdowncell>

# Some of the difficulties of finding mirrors start to appear here. We have around 100 videos with no title! 175 videos just called 'anonymous' -- what operation do they belong to, if any?
# 
# The good news is that there are many cases where the standard 'Anonymous Operation X' pattern holds. We can work with those as long as we keep in mind that we are losing several hundred potential mirrors in the process.

# <codecell>

# the pure operations videos
# videos that have the 'anonymous operation x' pattern
ops_pure = ops.ix[ops.title_clean.str.contains('anonymous operation')]
ops_pure.shape

# <markdowncell>

# ### Using durations to detect mirrors

# <codecell>

# might be better to cross check with other fields such as duration, publishedAt, etc
ops_pure = yt.format_durations(ops_pure)
ops_pure.duration_second.value_counts().plot(kind='bar')

# <codecell>

ops_pure.duration_second.value_counts()

# <markdowncell>

# This suggests that durations could be some help. There are 60 videos that are 565 secs, 58 that are 152 secs, etc. If titles have some match, and durations are close, then is that a mirror?

# <codecell>

def mirror_match

# <markdowncell>

# ## Quantifying mirroring on Anonymous
# 
# This leaves us with a dataset of 2800 videos to look at. Bear in mind this does not include the videos that do not use the term 'operation'. But it does answer the initial question we had. For around 80 Anonymous operations, there are at least 2800 mirrors. 

# <codecell>

print('Most mirrored operations:\n')
print(ops_pure.title_clean.value_counts()[:10])

# <codecell>

print('Least mirrored operations:\n')
print(ops_pure.title_clean.value_counts()[-10:])

# <markdowncell>

# The good thing about this list now is that it does seem to have much 'media noise' in it. This list looks like pure anonymous.  Only in operations that seem to have no mirrors does noise appear. 

# <codecell>

pl = plt.figure(figsize = (10,4))
title_counts = ops_pure.title_clean.value_counts().values
title_counts = title_counts[title_counts>1]
xval = range(0,len(title_counts))
yval = title_counts
plt.bar(xval, yval)
plt.title('Overview of mirrors/operation')
plt.xlabel('Operation number')
plt.ylabel('Mirror count')

# <codecell>

len(title_counts)

# <markdowncell>

# This suggests that operations have anywhere between 36 and 1 mirrored videos. But there are still too many  titles for operations.  There are around 370 unique titles of videos that fit the 'operation anonymous X' pattern, but we know of only around 80 Anonymous operations. What is overflowing here?

# <codecell>

# begin to see the problem here -- titles are mangled in various ways
print(ops_pure.title_clean.unique())

# <codecell>

# if we only look at the first three words?
ops_pure['title_short'] = ops_pure.title_clean.map(lambda x: ' '.join(x.split(' ')[:3]))

print(ops_pure.title_short.value_counts())
print(sum(ops_pure.title_short.value_counts()>1))

# <markdowncell>

# OK, that's a bit better. 240 operations appearing now. We might need to consider the possibility that our operations list is nowhere near complete

# <codecell>

ops_pure.title_short.to_csv('ops_list_to_check.csv')

# <markdowncell>

# This is obviously still not clean enough because many of the titles do not begin with 'anonymous operation'. Need to apply a stricter filder

# <codecell>

ops_pure2 = ops_pure.ix[ops_pure.title_clean.str.startswith('anonymous operation')]
ops_pure2['title_short'] = ops_pure2.title_clean.map(lambda x: ' '.join(x.split(' ')[:3]))

print(ops_pure2.title_short.value_counts())
print(sum(ops_pure2.title_short.value_counts()>1))

# <markdowncell>

# So now we are down to 220 operations.

# <codecell>

print(ops_pure2.title_short.value_counts())
f = open('data/found_operations.csv', 'wb')
f.writelines('\n'.join(ops_pure2.title_short.unique()))

# <codecell>


# <markdowncell>

# Ook, 

