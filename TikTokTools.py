'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-02 20:45:26
 # @ Description:
 '''

from TikTokApi import TikTokApi

class TikTokTools():
    '''
    TikTok Tools Class leverages TikTokApi heavily

    https://github.com/davidteather/TikTok-Api
    '''
    def __init__(self, verbosity=0, **kwargs):
        self.api = TikTokApi(**kwargs)
        self.videos = []
        self.requested_length = 0
        # Verbosity 0 = no print
        # Verbosity 1 = print statements
        # Verbosity 2 = extra verbose
        self._verbosity = verbosity

    def _check_video_shorter_than(self, video_entry):
        '''
        Returns boolean if video is less than given length
        '''
        res = video_entry['video']['duration'] < self.requested_length
        if self._verbosity:
            print(f"Video shorter than {self.requested_length}: {res}")
        return res

    def _check_video_not_in_list(self, video):
        '''
        Returns boolean if video being checked is in self.videos
        '''
        not_in_list = None
        for entry in self.videos:
            if self._verbosity == 2:
                print(f'_check_video_not_in_list video:\n\n{video}\n\nentry:\n\n{entry}')
            if video['id'] == entry['id']:
                not_in_list = False
            else:
                not_in_list =  True
        if not self.videos:
            not_in_list = True
        if self._verbosity:
            print(f'not_in_list {not_in_list}')
        return not_in_list

    def get_video_list(self, num_videos_requested, length_seconds):
        '''
        Return video list
        videos (list): list of dictionary tiktok objects
        '''
        # TODO BUG every time a new video is requested, it always retrieves
        # the first video in a list somewhere that is always the same. Need
        videolist_raw = self.api.trending(count=20, custom_verifyFp="")
        # to retrieve unique video.
        # HOTFIX: Retrieve a list of 20, 30, 50 videos and parse through each
        # of those as the results.
        self.requested_length = length_seconds
        for video in videolist_raw:
            # TODO eventually implement where new video is retrieved until list
            # is full
            # while len(self.videos) < num_videos_requested:
            self._add_video(video)
        return self.videos

    def _add_video(self, video):
        '''
        Add new video to self.videos list
        '''
        not_in_list = self._check_video_not_in_list(video)
        is_shorter = self._check_video_shorter_than(video)
        added_video = None
        if (is_shorter and not_in_list): 
            self.videos.append(video)
            added_video = True
        else:
            added_video = False
        if self._verbosity:
            print(f'added_video {added_video}')
        return added_video

    # ~~~~~~~~~~~~~~~~~~~ TODO List ~~~~~~~~~~~~~~~~~~~ #
    '''
    1. get_video_list bug
    2. Implement get videos by keyword search

    '''
    
