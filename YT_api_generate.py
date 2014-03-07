# %load_ext autoreload
# %autoreload 2

from apiclient.discovery import build
import apiclient.errors
import requests
import pandas as pd 
import re
import datetime
from datetime import datetime, timedelta

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API.

DEVELOPER_KEY = open('api.txt').readline()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#sample get:
#https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key=YOUR_API_KEY&part=snippet,contentDetails,statistics,status

def youtube_get_video_details(videoIds):

  """
  returns a pd.DataFrame of details about given videos;
  API only allows 50 ids at a time

  Parameters
  ---------------------------------------
  videoId: list of videoIds
  """

  base_url = 'https://www.googleapis.com/youtube/v3/videos?id='
  part_url = '&part=snippet,contentDetails,topicDetails,statistics,status'
  middle_url = ''.join(['&key=',DEVELOPER_KEY, part_url])
  id_strings = [','.join(s) for s in [videoIds[i:i+50]  for i in xrange(0, len(videoIds), 50)]]
  df = pd.DataFrame()
  for id_string in id_strings:
    full_url = ''.join([base_url,id_string,middle_url])
    response = requests.get(full_url).json()
    if 'items' in response:
      di1= {i['id']:i['statistics']  for i in response['items'] if i.has_key('statistics')}
      di2= {i['id']:i['contentDetails']  for i in response['items'] if i.has_key('contentDetails')}
      dft1= pd.DataFrame(di1.values(), index= di1.keys())
      dft2 = pd.DataFrame(di2.values(), index= di2.keys())
      di3= {i['id']:i['topicDetails'] for i in response['items'] if i.has_key('topicDetails')}
      dft3 = pd.DataFrame(di3.values(), index= di3.keys())
      dft = pd.concat([dft1, dft2, dft3], axis=1)
      df = df.append(dft)
  
  # print('Video statistics: ' + str(df.shape[0]))

  df['videoId'] = df.index
  # df = format_durations(df)
  return df


def youtube_video_details (videoId):

  """
  returns a pd.DataFrame of details about given videos;
  API only allows 50 ids at a time.
  But this version often throws errors -- something to do with the 
  apiclient.discovery module? Anyway, the function above - youtube_get_video_details
  -- now does a better job

  Parameters
  ---------------------------------------
  videoId: list of videoIds
  """
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  #break the ids into chunks of 50
  id_strings = [','.join(s) for s in [videoId[i:i+50]  for i in xrange(0, len(videoId), 50)]]
  df = pd.DataFrame()

  for id_string in id_strings:  

  # not sure what is going on here -- reimplement using Requests?
    try:
      query_function = youtube.videos().list(
        id = id_string,
        part = "id,statistics,contentDetails,topicDetails"
      )
      response =query_function.execute()
    except (AttributeError, apiclient.errors.HttpError),  h:
      print(h)
      print(query_function)

    print('getting video statistics: ' + str(df.shape[0]))

    # debug=True

    # if debug:
    #   return response

    di1= {i['id']:i['statistics']  for i in response['items']}
    di2= {i['id']:i['contentDetails']  for i in response['items']}
    dft1= pd.DataFrame(di1.values(), index= di1.keys())
    dft2 = pd.DataFrame(di2.values(), index= di2.keys())
    di3= {i['id']:i['topicDetails'] for i in response['items'] if i.has_key('topicDetails')}
    dft3 = pd.DataFrame(di3.values(), index= di3.keys())
    dft = pd.concat([dft1, dft2, dft3], axis=1)
    df = df.append(dft)

  df['videoId'] = df.index
  return df


def format_durations(df):
  """YouTube API durations come in the form 'PT34M22S'
  This function formats them as times, and returns a DataFrame
  with a time column added
  """
  splitter = re.compile('\D{1,3}')
  dur = df.duration.apply(splitter.split)
  hms = list()
  for d in dur:  
    if len(d) == 4:
      hms.append(datetime.strptime(':'.join([e.zfill(2) for e in d]), "%H:%M:%S:%f"))
    elif len(d) == 5:
      hms.append(datetime.strptime(':'.join([e.zfill(2) for e in d]), "%W:%H:%M:%S:%f"))
    elif len(d) == 3:
      hms.append(datetime.strptime(':'.join([e.zfill(2) for e in d]), "%M:%S:%f"))
  df['duration_time'] = hms
  df['duration_second'] = df['duration_time'].apply(lambda x:  x.hour*3600+x.minute*60 + x.second)
  return df

def convert(s):
             t = datetime.strptime(s, "%M:%S")
             return t.minute*60 + t.second

def youtube_search(query, max_results=1000, with_statistics = False):

  """
  Returns a pd.DataFrame of results giving titles, description, ids, etc

  Parameters 
  ---------------------------------------------
  query: the query term
  max_results: the number of values to return
  with_statistics: whether to ask for viewing statistics
  """

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    type='video',
    maxResults=50
  ).execute()

  di={i['id']['videoId']:i['snippet'] for i in search_response['items']}
  df = pd.DataFrame(di.values(), index = di.keys())


  # to retrieve more pages need to loop through nextPageTokens
  while search_response.has_key('nextPageToken') and  df.shape[0] <max_results:
    nextPage = search_response['nextPageToken']
    search_response = youtube.search().list(
      q=query,
      part="id,snippet",
      type='video',
      pageToken = nextPage,
      maxResults=50
    ).execute()
    dit={i['id']['videoId']:i['snippet'] for i in search_response['items']}
    dft  = pd.DataFrame(dit.values(), index = dit.keys())
    df = df.append(dft, ignore_index=False)
  
  df['videoId'] = df.index
  print ('retrieved ' + str(df.shape[0]) + ' results for ' + query)
  #check if any rows are returned
  if df.shape[0] >0:
    if with_statistics:
      df_stats = youtube_get_video_details(df.videoId)
      print(query, df_stats.shape)
      print(df.shape)
      df = pd.merge(df, df_stats)

    #cleaning up
    df.title=[t.encode('utf8', errors='ignore') for t in df.title]
    df.description=[t.encode('utf8', errors='ignore') for t in df.description]
  
  return df

