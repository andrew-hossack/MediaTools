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
    tt = TikTokTools(verbosity=1)
    vt = VideoTools()

    num_videos_requested = 3    # Max number of return videos
    max_length_seconds = 20     # Max length of videos returned
    buffer_length = 10          # Temporary fix to make sure enough videos are added to buffer
                                # Buffer is an un-filtered list of video instances 
                                # Consider implementing method to get new videos each time
    videolist_parsed = tt.get_video_list(num_videos_requested, max_length_seconds, buffer_len=buffer_length)

    for obj in videolist_parsed:
        # Get new video from list
        desc = tt.get_video_description(obj)
        downloadaddr = tt.get_video_download_address(obj)
        author = tt.get_video_author(obj)
        print(f"Title: {desc} by {author}\nLink: {downloadaddr}")

        # Download Video
        vt.video_downloader_from_url(downloadaddr)
        print(f'Done Downloading to {vt._downloads_dir}\n')