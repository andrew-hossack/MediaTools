'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-02 20:55:32
 # @ Description:
 '''

from common.TikTokTools import TikTokTools
from common.VideoTools import VideoTools

def main(**kwargs):
    api = TikTokTools(verbosity=0)
    num_videos_requested = kwargs.get('num_videos_requested', 5)
    length_seconds = kwargs.get('length_seconds', 15)

    videolist_parsed = api.get_video_list(num_videos_requested, length_seconds, buffer_len=5)

    for tiktok in videolist_parsed:
        # Prints the id of the tiktok
        print(f"Title: {tiktok['desc']} by {tiktok['author']['nickname']}\nLink: {tiktok['video']['playAddr']}\n\n")

if __name__ == "__main__":
    main()