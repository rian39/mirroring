# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Exploration of the Anonymous videos on Youtube. 
# 
# ## How the initial data was generated (by Davide Beraldo)
# 
# The query: "anonymous internet freedom"
# 
# Some notes: I have just discovered that some changes have been made to YT api, so the script was not able to retreive keywords associated with videos (that can be interesting for semantic network analysis purposed) and that videos descriptions are truncated. I will try to figure out whether is possible to fix the first shortcome; for the second, luckly the "related videos" descriptions are still complete..and usually there is wide redundancy, so maybe it can be easily overcame (consider that in this sample I restricted related videos to 25 for each); the comments are also in this case limited to 25; videos are ordered by relevance computed by Youtube itself; users are limited to original content submitters; the string I input as keyword was only "anonymous internet freedom".
# 
# (1) retrieve up to 1000 videos queried by keywords (including username,date,category,n of favorites, n of views,duration, tags and description)
# -maybe it is possible to extend the 1000 limit, or by the way it can be somehow done with the following module-
# 
# (2) reconstruct the network of "related videos" for each video retrieved (with the metadata above)
# -the alghoritm for matching related videos is of course not known, but as far as I understood it should be both related to tags and to users' behaviour: the more two videos are viewed in sequence, the more related they'll be... so it can provide interesting insights on network of content-
# 
# (3) scrape comments related to the videos/related videos retrieved (including user name, time and parent comments) 
# The geo info are quite tricky cause there is no "nationality" associated to the video, but the language...at least not provided with the api! But maybe something can be inferred with a heuristic approach (nations mentioned in the title/description/comments)

# <codecell>

import pandas as pd
from pylab import *
from IPython.display import HTML
from IPython.display import YouTubeVideo
pd.set_option("display.max_columns", 6)
pd.set_option("display.max_rows", 15)
pd.set_option("display.notebook_repr_html", True)

# <codecell>

an_f = pd.ExcelFile('data/anonymouys internet freedom - VIDEOS.xls')
an_dict = {name:an_f.parse(name) for name in an_f.sheet_names}
video_df = an_dict['VIDEOS']
#clean up data a bit
video_df.VIEWS = video_df.VIEWS.replace('None', 0)
video_df.shape

# <codecell>

print('Users: ', len(video_df.USER.unique()))
print('Titles: ', len(video_df.TITLE.unique()))

# <markdowncell>

# ## Shape of the video data
# 
# There are 908 titles in the dataset, of which 283 are unique. There are 246 users -- people (robots?) who upload videos.

# <markdowncell>

# ## The length of the videos
# 
# Not sure what the length of videos tells us. Something about the kind of object we are dealing with. Also, I guess length affects mirroring. Would many people upload a 60 minute documentary?

# <codecell>

duration = video_df.DURATION.order().tolist()
duration = [d/60 for d in duration]
f = pylab.figure(figsize=(10,5))
sp=f.add_subplot(1,1,1)

h=sp.hist(duration, bins=100)
print('Less than 10 minutes: '+ str(float(sum(video_df.DURATION/60 < 10))/video_df.DURATION.shape[0]*100)+ '%')
sp.set_title('Length of videos (minutes)')
sp.set_xlabel('minutes')
sp.set_ylabel('videos')
YouTubeVideo(video_df.ID.iloc[1])

# <markdowncell>

# This looks like most of the videos are relatively short (less than 10 minutes). Does duration correlate with either viewing or duplication?

# <codecell>

fig=figure(dpi=200)
sp = fig.add_subplot(1,1,1)
sp.scatter(video_df.DURATION/60, video_df.VIEWS, s=5,marker='o')
sp.set_title('Duration vs Views')
sp.set_xlabel('Duration (minutes)')
sp.set_ylabel('Views')
sp.set_xlim(0, 200)
sp.set_ylim(0, 1e7)

# <markdowncell>

# At a glance, it looks like the longer videos are viewed much less. Very short videos are not viewed much either. But this doesn't take into account the fact that there are many more short videos. 

# <markdowncell>

# # Viewing figures
# 
# Another way to look at videos -- more in terms of reception. What stands out here?

# <codecell>

video_df.VIEWS = video_df.VIEWS.replace('None', 0)
views = video_df.VIEWS.order()
f=figure(figsize(10,5))
suptitle('Views of videos at different scale')
sp1 = f.add_subplot(1,3,1)
h1=sp1.hist(views, bins=100)
sp1.set_ylabel('Number of videos')
sp1.set_xlabel('Number of views')
sp1.set_title('View high scale')
sp2 = f.add_subplot(1,3,2)
h2 = sp2.hist(views[views<100], bins=100)
sp2.set_title('View on medium scale')
sp2.set_ylabel('Number of videos')
sp2.set_xlabel('Number of views')
sp3 = f.add_subplot(1,3,3)
h3 = sp3.hist(views[views<10], bins = 10)
sp3.set_title('View on low scale')
sp3.set_ylabel('Number of videos')
sp3.set_xlabel('Number of views')

# <markdowncell>

# As usual, most videos are only viewed by a small number of people, and a couple are viewed by 100,000s up to 14 million. Actually, viewing figures are quite widely distributed even for the less-viewed videos. It might be interesting to look at the videos that are viewed 8, 30 or 80 times as well as the ones viewed 14 millon times. This analysis _does not_ take into account view figures for copies of videos.
# 
# ## The most viewed videos
# 
# If we aggregate views for videos with the same title, things start to look different. 

# <codecell>

top_views = video_df.loc[video_df.VIEWS>100000, ['TITLE', 'VIEWS']]
gby=top_views.groupby(by='TITLE')['VIEWS']
print('total viewings:'+str(video_df['VIEWS'].sum()))
print('total views of top videos:', sum(gby.sum()))
print('total views of top 5 videos:', sum(gby.sum()[:4]))

print(gby.ngroups)
gbyo=gby.sum().order(ascending=False)
pie(gbyo[0:9], labels=gbyo.keys()[0:9])
pylab.title('Most viewed videos in terms of view share')
pd.DataFrame(gbyo).head(n=5)

# <markdowncell>

# There are 18 videos that each have more 100,00 views. There have been around 480 million views in total of Anonymous-related videos. The top 18 videos account for 477 million of the views. The top 5 videos account for 460 million of the 480 million. 
# Looking at the titles, is the 'Emmanuel Kelly X Factor 2011 Auditions' video 'noise'? Maybe not -- he's an Iraqi orphan living in Australia, and 'Collateral Murder - Wikileaks - Iraq' (#2) doesn't look like that. The top four videos after Kelly's all have more than 50 million viewings. So they dominate the total views of Anonymous videos. 

# <codecell>

#video_df.TITLE.
emmanuel_kelly = video_df.ID[video_df.TITLE == gbyo.index[0]]
YouTubeVideo(emmanuel_kelly.iloc[0])

# <markdowncell>

# ## Are video duplicates viewed?
# 
# Are views related to duplication/mirroring practices? First, we need to find the duplicates. Title is an ok starting point. Presumably, videos with the same title are likely to be duplicates.

# <codecell>

title = video_df.TITLE.tolist()
video_df.TITLE = [t.encode('utf8', errors='ignore') for t in title]
print('distinct titles:', len(video_df.TITLE.unique()))
print('distinct ids', len(video_df.ID.unique()))
print('distinct durations:', len(video_df.DURATION.unique()))

# <markdowncell>

# While there are 908 videos listed, there are only 283 distinctly titled videos and 289 distinct video IDS. That means that potentially ~620 are copies. But if copies have the same ID, does that mean that they have been uploaded? Or are they simply different views on the same video? This is a crucial question - are we dealing here with duplicates or just references to one instance?  
# Things are a bit more complicated in the duration data. There are only 220 distinct durations. But it could be that different videos happen to have the same duration. 
# What are the most commonly duplicated videos?

# <codecell>

dup_video_counts =video_df.TITLE.value_counts()
dup_df = pd.DataFrame(dup_video_counts.head())
dup_df

# <codecell>

top_dup_video_counts=dup_video_counts[dup_video_counts>5]
top_dup_video_counts = top_dup_video_counts.order(ascending=False)
top_dup_videos = dup_video_counts.index
top_dup_video_counts

# <markdowncell>

# Does duplication correlate with viewing figures? Do these duplicates get the same number of views? Or are some versions much more widely viewed than others?

# <codecell>

dup_views=video_df.loc[video_df.TITLE.isin(top_dup_videos), ['TITLE', 'VIEWS']]
dup_views['copies'] = top_dup_video_counts
dv =pd.DataFrame(dup_views.groupby(['TITLE'])['VIEWS'].sum().order(ascending=False))
dv.head()

# <markdowncell>

# Some interesting points here. High rates of duplication does not equate with high view counts. What is the Christopher Hitchens piece? It is the 4th most duplicated video, but shows 0 views - is that possible? More importantly, the most duplicated video 'Anonymous - Truth is a Virus' only has 1380 views.
# 
# ## TBC -- look at views and copies side by side

# <markdowncell>

# ## Some stuff on users

# <codecell>

video_df.columns
video_df['USER'].unique().shape

# <markdowncell>

# So there are 246 users (people?) who upload videos. How much do they upload?

# <codecell>

user_counts = video_df['USER'].value_counts()
f3 = figure(figsize=(5,3))
sp=f3.add_subplot(111)
h4 = sp.hist(video_df['USER'].value_counts(), bins=100)
sp.set_title('Number of videos per user')
top_users = user_counts[user_counts>5].index
top_users
print(user_counts.describe())
user_counts.quantile(0.6)

# <markdowncell>

# So, more than 60% of people upload less than 2 videos. 

# <markdowncell>

# ## How top contributing users upload top-viewed videos -- that is, do they duplicate them? 
# 
# I'm calling 'top users' anyone who uploads more than 5 videos, and 'top videos' any video that is duplicated more than 5 times. 

# <codecell>

topuser_toptitle=pd.crosstab(video_df[video_df.USER.isin(top_users)]['USER'], video_df[video_df.TITLE.isin(top_dup_videos)]['TITLE'])
top_user_title_df = pd.DataFrame(topuser_toptitle.sum(axis=1).order(ascending=False))
top_user_title_df.head()

# <markdowncell>

# This suggests that there is some link between between uploading a lot and duplicating a lot. I'm not sure about this actually -- needs further thought. There is still the question of whether the duplicates are viewed a lot. And do these high duplicating users duplicate the same videos?

# <markdowncell>

# ## What is viewed
# 
# Many questions could be asked here. For highly duplicated videos, are all copies viewed at similar levels or not?

# <codecell>

date = pd.to_datetime(video_df.DATA)
video_df.DATA = date
video_df.groupby(by=['TITLE'])['VIEWS'].sum().order()

# <codecell>

f = figure(figsize=(8,6), dpi=400)
s = f.add_subplot(111)
s.scatter(date, video_df.VIEWS)
s.set_title('Viewing activity over time')
s.set_ylabel('Views')

top_views.head()

# <markdowncell>

# Hard to see what is happening in the viewing of these videos. 

