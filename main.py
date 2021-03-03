from TikTokTools import TikTokTools
import dat.exampledict




def main(**kwargs):
    api = TikTokTools(verbosity=1)
    num_videos_requested = kwargs.get('num_videos_requested', 5)
    length_seconds = kwargs.get('length_seconds', 20)

    videolist_parsed = api.get_video_list(num_videos_requested, length_seconds)

    for tiktok in videolist_parsed:
        # Prints the id of the tiktok
        print(f"Title: {tiktok['desc']} by {tiktok['author']['nickname']}\nLink: {tiktok['video']['playAddr']}\n\n")

if __name__ == "__main__":
    main()