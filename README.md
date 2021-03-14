# MediaTools Content Creation Library
A project for automating the simple task of uploading mindless content to YouTube. This library is written to leverage different input video sources and includes resources like TikTokTools to get content. 

In the future, other sources of video, audio, and text-based content will be provided such as Reddit over Text To Speech (TTS) and more.

## Getting Started

### Installation Instructions
To install this package using pip, in the root directory *MediaTools/* run the command
```bash
pip install .
```

### Secrets Files
Some MediaTools classes require the use of client secrets json files. Currently, YouTubeTools.py, RedditTools.py and TTSTools.py need them. Please follow the instructions either listed in the specific class section below or as referenced in the class file itself to obtain a client secrets file.

## MediaTools Classes

### ```Managed Workspace```
WorkspaceManager.py is the base class for all MediaTools classes. This parent class has two basic attributes: *secrets_filepath* and *managed_path*. Secrets filepath can be specified as an absolute filepath to a json secrets file, or can be specified as none at class init in the child class.

```python
args:
    secrets_filepath (str):
        Absolute filepath of secrets json file to load
kwargs:
    managed_path (str):
        Managed directory name from root
        Defaults to /dat
```

The managed filepath points to a basic directory to store all MediaTools files in. It defaults to *root/dat*.

### ```TikTokTools Class```
Built on [TikTokApi by David Teather](https://github.com/davidteather/TikTok-Api), ```TikTokTools``` is a wrapper class to enable the user to quickly source content from TikTok without needing developer API access. 

The main method is ```get_video_list```. This method takes in a number of arguments and returns a list of TikTok dictionary objects. Please see below for an example of a TikTok Dictionary object.

#### Examples
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

#### Dictionary Object
For the sake of space, an example TikTok dictionary object can be found here: [https://gist.github.com/davidteather/7c30780bbc30772ba11ec9e0b909e99d](https://gist.github.com/davidteather/7c30780bbc30772ba11ec9e0b909e99d)

### ```VideoTools Class```
A helper tools class for video processing, ```VideoTools``` contains several useful methods for downloading and parsing video content, as well as directory data management and configuration management.

Videos and data that are being manipulated through this library shall be stored in *TikTok/dat/* file location. Note that upon instantiating the class, all data from this location **will be removed!**

Video data will be stored in a configuration file. More information can be seen below.

#### Configuration Management
Video configuration settings shall be stored in *TikTok/video.yaml* file. Currently, only video title, decription, and author as well as optional metadata tags are stored. 

Upon initialization, this configuration file will be loaded into the class. If a user makes a change to the yaml file during application runtime, they will need to call ```get_updated_config_data``` to update class info.

#### Examples
One helpful method is ```video_downloader_from_url(download_url)```. This method will download videos to *downloads_dir_*. 

```python
videoInstance = VideoTools()
print(videoInstance.author)

# Download Video
videotools.video_downloader_from_url(downloadaddr)
```

Another helpful method is ```update_config(updated_dict)```. This method can be used to safely update ```video.yaml``` file.

```python
updated_dict = {
    'video': {
        'title':'123455'
        }
    }
vt.update_config(updated_dict)
```

### ```YouTubeTools Class```
A wrapper class for ```googleapiclient``` [https://developers.google.com/youtube/v3/guides/uploading_a_video](https://developers.google.com/youtube/v3/guides/uploading_a_video
), this class adds functionality to upload videos to YouTube.

Make sure you have included the OAuth 2.0 ```youtube_client_secrets.json``` absolute filepath during class instantiation.

#### Upload Keyword Args
Please see ```__init__``` for more details.

- filepath (str)
- title (str)
- description (str)
- category (str)
  - [https://developers.google.com/youtube/v3/docs/videoCategories/list](https://developers.google.com/youtube/v3/docs/videoCategories/list)
- keywords (str)
- privacyStatus (str)
  - Valid values are public, private, and unlisted
- videoDir (str): Directory of video to upload

#### Examples

```python
instance = YouTubeTools(file='video.mp4')
youtube = instance.get_authenticated_service()

# Try to upload a file out.mp4 located in /dat
try:
    instance.initialize_upload(youtube)
except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
```

### ```RedditTools Class```
A wrapper class for PRAW [https://praw.readthedocs.io/en/latest/](https://praw.readthedocs.io/en/latest/). Upon init, this class will load in secrets data from ```private/reddit_client_secrets.json```. For more information on reddit client secrets, please see [https://github.com/reddit-archive/reddit/wiki/OAuth2](https://github.com/reddit-archive/reddit/wiki/OAuth2).

To get a new refresh token, you can run the python file found at ```lib/refreshtokengen.py```.

#### Examples
Before using this class, make sure to fill in client secrets!

```python
rt = RedditTools()
url = 'https://www.reddit.com/r/redditdev/comments/hasnnc/where_do_i_find_the_reddit_client_id_and_secret/'
rt.set_url(url)

# Get info from post
title = rt.get_title()
author = rt.get_author()
text = rt.get_selftext()

print(f'{title} by {author}\n{text}')
```

### ```TTSTools Class```
Text To Speech (TTS) Tools ```TTSTools``` class is a helper class and wrapper for using Google wavenet Text To Speech. More information about the google tts client libraries can be found at the link [https://cloud.google.com/docs/authentication/production](https://cloud.google.com/docs/authentication/production).

The main functionality of this class is to synthesize lifelike voice from a text entry.

#### Examples

```python
# Instantiate TTSHelper and save outfile to dat/audio.mp3
tts = TTSHelper(outfile_name='audio.mp3')

# Load in text file
with open('dat/exampletextfile.txt') as file:
  # Synthesize speech
  tts.synthesize_text(file)
```