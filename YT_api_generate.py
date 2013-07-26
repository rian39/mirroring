# %load_ext autoreload
# %autoreload 2


from apiclient.discovery import build
from optparse import OptionParser
import pandas as pd

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBFAnShIZy8_McvshPS3o9uac8ZODaktcA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#sample get:
#https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key=AIzaSyBFAnShIZy8_McvshPS3o9uac8ZODaktcA&part=snippet,contentDetails,statistics,status

def youtube_search(options, query = ''):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  if query != '':
    options.q = query

  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    type='video',
    maxResults=options.maxResults
  ).execute()

  di={i['etag']:i['snippet'] for i in search_response['items']}
  df = pd.DataFrame(di.values(), index = di.keys())

  # to retrieve more pages
  nextPage = search_response['nextPageToken']

  while nextPage != None and  df.shape[0] <5000:
    search_response = youtube.search().list(
      q=options.q,
      part="id,snippet",
      type='video',
      maxResults=options.maxResults
    ).execute()
    dit={i['etag']:i['snippet'] for i in search_response['items']}
    print ('getting another page of results ... ' + str(df.shape[0]))
    dft  = pd.DataFrame(dit.values(), index = dit.keys())
    df = df.append(dft, ignore_index=True)
    nextPage = search_response['nextPageToken']
  return df

def test():
  parser = OptionParser()
  parser.add_option("--q", dest="q", help="Search term",
    default="Google")
  parser.add_option("--max-results", dest="maxResults",
    help="Max results", default=25)
  (options, args) = parser.parse_args()
  return youtube_search(options)

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("--q", dest="q", help="Search term",
    default="Google")
  parser.add_option("--max-results", dest="maxResults",
    help="Max results", default=25)
  
  (options, args) = parser.parse_args()

  youtube_search(options)