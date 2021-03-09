'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-07 11:50:20
 # @ Description: Reddit tools class
 '''

import json
import os
from pathlib import Path
import praw
from prawcore.exceptions import RequestException
from praw.models import MoreComments
import sys

class RedditTools:
    '''
    Wrapper class for praw
    https://praw.readthedocs.io/en/latest/
    '''
    def __init__(self, secrets_filepath):
        '''
        args:
            secrets_filepath (str):
                Absolute path to secrets file

        callables:
            self.prawclient (praw): PRAW Client instance
            self.submission (post): PRAW post object, must call
                                    set_url(url) to use other methods
        '''
        self._secrets_dir = Path(secrets_filepath)
        with open(self._secrets_dir) as redditsecrets:
            self._secrets = json.load(redditsecrets)
        self.prawclient = praw.Reddit(client_id=self._secrets['web']['client_id'], 
                            client_secret=self._secrets['web']['client_secret'],
                            refresh_token=self._secrets['web']['refresh_token'],
                            user_agent=self._secrets['web']['user_agent'])
        self.submission = None

    def set_url(self, url):
        '''
        Set URL of reddit post - must call before using other functions!
        '''
        self.submission = self.prawclient.submission(url=url)

    def get_author(self):
        '''
        Get author of post
        author (str)
        '''
        if self.submission:
            return str(self.submission.author)

    def get_time_created(self):
        '''
        (str): Time the submission was created, represented in `Unix Time`_.
        '''
        if self.submission:
            return str(self.submission.created_utc)

    def get_title(self):
        '''
        Get title of post
        '''
        if self.submission:
            return str(self.submission.title)

    def get_selftext(self):
        '''
        The submissions' selftext - an empty string if a link post.
        '''
        if self.submission:
            return str(self.submission.selftext)