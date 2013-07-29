# %load_ext autoreload
# %autoreload 2


from apiclient.discovery import build
from optparse import OptionParser
import pandas as pd
import apiclient.errors
import requests

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = open('api.txt').readline()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#sample get:
#https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key=YOUR_API_KEY&part=snippet,contentDetails,statistics,status

def youtube_get_video_details(videoIds):

  base_url = 'https://www.googleapis.com/youtube/v3/videos?id='
  part_url = '&part=snippet,contentDetails,topicDetails,statistics,status'
  middle_url = ''.join(['&key=',DEVELOPER_KEY, part_url])
  id_strings = [','.join(s) for s in [videoIds[i:i+50]  for i in xrange(0, len(videoIds), 50)]]
  df = pd.DataFrame()
  for id_string in id_strings:
    full_url = ''.join([base_url,id_string,middle_url])
    response = requests.get(full_url).json
    if 'items' in response:
      di1= {i['id']:i['statistics']  for i in response['items'] if i.has_key('statistics')}
      di2= {i['id']:i['contentDetails']  for i in response['items'] if i.has_key('contentDetails')}
      dft1= pd.DataFrame(di1.values(), index= di1.keys())
      dft2 = pd.DataFrame(di2.values(), index= di2.keys())
      di3= {i['id']:i['topicDetails'] for i in response['items'] if i.has_key('topicDetails')}
      dft3 = pd.DataFrame(di3.values(), index= di3.keys())
      dft = pd.concat([dft1, dft2, dft3], axis=1)
      df = df.append(dft)
    print('getting video statistics: ' + str(df.shape[0]))

  df['videoId'] = df.index
  return df



def youtube_video_details (videoId):

  """
  returns a pd.DataFrame of details about given videos;
  API only allows 50 ids at a time
  ---------------------------------------
  options: the request parameters
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


def youtube_search(query, max_results=1000, with_statistics = False):

  """
  Returns a pd.DataFrame of results giving titles, description, ids, etc

  Parameters 
  ---------------------------------------------
  options: the api options
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
    print ('getting another page of results ... ' + str(df.shape[0]))
    dft  = pd.DataFrame(dit.values(), index = dit.keys())
    df = df.append(dft, ignore_index=False)
  
  df['videoId'] = df.index
  
  if with_statistics:
    df_stats = youtube_get_video_details(df.videoId)
    print(df_stats.shape)
    print(df.shape)
    df = pd.merge(df, df_stats)

  #cleaning up
  df.title=[t.encode('utf8', errors='ignore') for t in df.title]
  df.description=[t.encode('utf8', errors='ignore') for t in df.description]
  
  return df

# def test():
#   parser = OptionParser()
#   parser.add_option("--q", dest="q", help="Search term",
#     default="Google")
#   parser.add_option("--max-results", dest="maxResults",
#     help="Max results", default=25)
#   (options, args) = parser.parse_args()
#   return youtube_search(options)

# def setOptions():
#   parser = OptionParser()
#   parser.add_option("--q", dest="q", help="Search term",
#     default="Google")
#   parser.add_option("--max-results", dest="maxResults",
#     help="Max results", default=50)
#   options= parser.parse_args()[0]
#   return options

# if __name__ == "__main__":
#   options = setOptions()
#   youtube_search(options)