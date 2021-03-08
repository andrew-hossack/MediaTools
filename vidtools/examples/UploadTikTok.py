'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-02 20:55:32
 # @ Description: Driver file for uploading TikTok videos.
        Feel free to build off of this as an example!
 '''

from vidtools.TikTokTools import TikTokTools
from vidtools.VideoTools import VideoTools
from vidtools.YouTubeTools import YouTubeTools

# NOTE This driver file is NOT COMPLETE!

if __name__ == "__main__":
    tt = TikTokTools()
    vt = VideoTools()
    ytt = YouTubeTools('/Users/andrew/Documents/VidTools/vidtools/private/reddit_client_secrets.json')

    videolist_parsed = tt.get_video_list(
        num_videos_requested=1, 
        max_length_seconds=20, 
        buffer_len=10 )

    for obj in videolist_parsed:
        # Get new video from list
        desc = tt.get_video_description(obj)
        downloadaddr = tt.get_video_download_address(obj)
        author = tt.get_video_author(obj)
        print(f"Title: {desc} by {author}\nLink: {downloadaddr}")

        # Download Video
        vt.video_downloader_from_url(downloadaddr)
        print(f'Done downloading to {vt._downloads_dir}\n')
    
    