'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-02 20:55:32
 # @ Description: Driver file for uploading TikTok videos.
        Feel free to build off of this as an example!
 '''


from googleapiclient.errors import HttpError
from mediatools.TikTokTools import TikTokTools
from mediatools.VideoTools import VideoTools
from mediatools.YouTubeTools import YouTubeTools


if __name__ == "__main__":
    # Instantiate video resources
    tt = TikTokTools()
    vt = VideoTools()
    ytt = YouTubeTools('/Users/andrew/Documents/MediaTools/mediatools/private/reddit_client_secrets.json')

    # Get parsed videolist with one video, no more than 20 seconds long
    videolist_parsed = tt.get_video_list(
        num_videos_requested=1, 
        max_length_seconds=20, 
        buffer_len=10)

    # Do work on the video list; print out information 
    for obj in videolist_parsed:

        # Get title, author and download url info from videos
        title = tt.get_video_description(obj)
        url = tt.get_video_download_address(obj)
        author = tt.get_video_author(obj)
        print(f"Title: {title} by {author}\nLink: {url}")

        # Download the video to local managed cache
        # Video out name will be set to TikTok.mp4
        vt.video_downloader_from_url(url, title='TikTok')
        print(f'Done downloading to {vt._downloads_dir}\n')
    
    # Load in video title and author information
    # In this case, it would be easier to specify this info by hand,
    # but it would make sense in other cases to do it programatically
    print(f'Current config:')
    vt.pp_config()

    video_info = {
                'video': {
                    'title':'Test Title Goes Here'
                    }
                }
    vt.update_config(video_info)

    print('The new config looks like this:')
    vt.pp_config()

    # Get video information from mediatools config
    title = vt.title
    author = vt.author
    description = vt.description
    tagslist = vt.tags

    # File to upload is 'TikTok.mp4', downloaded earlier
    # You do not have to specify directory - it is handled automatically!
    # A full list of upload args can be found in YouTubeTools init
    instance = YouTubeTools(
        file='TikTok.mp4',
        title=title,
        description=description,
        keywords=tagslist)
    
    # Try an upload with youtube instance
    youtube = instance.get_authenticated_service()
    try:
        instance.initialize_upload(youtube)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
