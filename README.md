# YouTube Automation Project
A project for automating the simple task of uploading mindless content to YouTube. This library is written to leverage different input video sources and includes resources like TikTokTools to get content. 

In the future, other sources of video, audio, and text-based content will be provided such as Reddit over Test To Speech (TTS) and more.

## ```TikTokTools Class```
Built on [TikTokApi by David Teather](https://github.com/davidteather/TikTok-Api), ```TikTokTools``` is a wrapper class to enable the user to quickly source content from TikTok without needing developer API access. 

The main method is ```get_video_list```. This method takes in a number of arguments and returns a list of TikTok dictionary objects. Please see below for an example of a TikTok Dictionary object.

### Examples
```python
def print_videos(**kwargs):
    # Instantiate API
    api = TikTokTools(verbosity=0)

    # num_videos_requested is number of videos you'd like to receive that are shorter than length_seconds
    # method will try to return as many videos as you request that fall within these parameters
    num_videos_requested = kwargs.get('num_videos_requested', 5)
    length_seconds = kwargs.get('length_seconds', 15)

    # Get parsed video list
    videolist_parsed = api.get_video_list(num_videos_requested, length_seconds, buffer_len=5)

    for tiktok in videolist_parsed:
        # Prints the id of the tiktok
        print(f"Title: {tiktok['desc']} by {tiktok['author']['nickname']}\nLink: {tiktok['video']['playAddr']}\n\n")

```

### Dictionary Object
For the sake of space, an example TikTok dictionary object can be found here: [https://gist.github.com/davidteather/7c30780bbc30772ba11ec9e0b909e99d](https://gist.github.com/davidteather/7c30780bbc30772ba11ec9e0b909e99d)

## ```VideoTools Class```
A helper tools class for video processing, ```VideoTools``` contains several useful methods for downloading and parsing video content, as well as directory data management and configuration management.

Videos and data that are being manipulated through this library shall be stored in *TikTok/dat/* file location. Note that upon instantiating the class, all data from this location **will be removed!**

Video data will be stored in a configuration file. More information can be seen below.

### Configuration Management
Video configuration settings shall be stored in *TikTok/video*.yaml_ file. Currently, only video title, decription, and author as well as optional metadata tags are stored. 

Upon initialization, this configuration file will be loaded into the class. If a user makes a change to the yaml file during application runtime, they will need to call ```get_updated_config_data``` to update class info.

### Examples
One helpful method is ```video_downloader_from_url(download_url)```. This method will download videos to *downloads_dir_*. 

```python
from common.VideoTools import VideoTools
videoInstance = VideoTools()
print(videoInstance.author)
```