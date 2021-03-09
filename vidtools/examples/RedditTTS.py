'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-07 20:27:39
 # @ Description: Reddit to TTS example
 '''

from vidtools.RedditTools import RedditTools
from vidtools.TTSTools import TTSHelper
import os

'''
Download a reddit post and convert to audio file for processing
'''

if __name__ == '__main__':
    
    rt = RedditTools('/Users/andrew/TikTok/vidtools/private/reddit_client_secrets.json')
    tts = TTSHelper('/Users/andrew/TikTok/vidtools/private/google_tts_secrets.json')

    # Get a post URL. Reference PRAW for other automated methods
    url = 'https://www.reddit.com/r/redditdev/comments/hasnnc/where_do_i_find_the_reddit_client_id_and_secret/'
    rt.set_url(url)

    # Get info from post
    title = rt.get_title()
    author = rt.get_author()
    text = rt.get_selftext()

    # Format reddit post text
    body = f'{title} by {author}. {text}'

    # Download body to /dat/audio.mp3
    tts.synthesize_speech(body)