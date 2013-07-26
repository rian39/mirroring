from apiclient.discovery import build
from optparse import OptionParser

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBFAnShIZy8_McvshPS3o9uac8ZODaktcA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#sample get:
#https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key=AIzaSyBFAnShIZy8_McvshPS3o9uac8ZODaktcA&part=snippet,contentDetails,statistics,status
def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

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

  while nextPage != Null:
    search_response = youtube.search().list(
      q=options.q,
      part="id,snippet",
      type='video',
      maxResults=options.maxResults
    ).execute()
    di={i['etag']:i['snippet'] for i in search_response['items']}
    dft  = pd.DataFrame(di.values(), index = di.keys())
    df = pd.concat(df, dft)
    nextPage = search_response['nextPageToken']


  # search_response = youtube.search().list(
  #   q=options.q,
  #   part="id,snippet",
  #   type='video',
  #   pageToken = nextPage,
  #   maxResults=options.maxResults
  # ).execute()

  # di2={i['etag']:i['snippet'] for i in search_response['items']}
  # df2= pd.DataFrame(di.values(), index = di.keys())
  # df_full = pd.concat([df, df2])

  # videos = []
  # channels = []
  # playlists = []

  # for search_result in search_response.get("items", []):
  #   if search_result["id"]["kind"] == "youtube#video":
  #     videos.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                search_result["id"]["videoId"]))
  #   elif search_result["id"]["kind"] == "youtube#channel":
  #     channels.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                  search_result["id"]["channelId"]))
  #   elif search_result["id"]["kind"] == "youtube#playlist":
  #     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                   search_result["id"]["playlistId"]))

  # print "Videos:\n", "\n".join(videos), "\n"
  # print "Channels:\n", "\n".join(channels), "\n"
  # print "Playlists:\n", "\n".join(playlists), "\n"


if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("--q", dest="q", help="Search term",
    default="Google")
  parser.add_option("--max-results", dest="maxResults",
    help="Max results", default=25)
  
  (options, args) = parser.parse_args()

  youtube_search(options)