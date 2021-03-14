'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-02 20:45:26
 # @ Description:
 '''


from TikTokApi import TikTokApi
from queue import Queue
from mediatools.WorkspaceManager import ManagedWorkspace


class TikTokTools(ManagedWorkspace):
    '''
    TikTok Tools wrapper for TikTokApi
    https://github.com/davidteather/TikTok-Api
    '''
    def __init__(self, verbosity=0, **kwargs):
        '''
        Verbosity:  0 = no print
                    1 = print statements
                    2 = extra verbose
        '''
        super().__init__(secrets_filepath=None)
        self._api = TikTokApi(**kwargs)
        self._videos = Queue()
        self._requested_length
        self._verbosity = verbosity

    def _check_video_shorter_than(self, video_entry):
        '''
        Returns boolean if video is less than given length
        '''
        res = video_entry['video']['duration'] < self._requested_length
        if self._verbosity:
            print(f"Video shorter than {self._requested_length}: {res}")
        return res

    def _check_video_not_in_list(self, video):
        '''
        Returns boolean if video being checked is in self.videos
        '''
        not_in_list = None
        while not self._videos.empty:
            entry = self._videos.get()
            if self._verbosity == 2:
                print(f'_check_video_not_in_list video:\n\n{video}\n\nentry:\n\n{entry}')
            if video['id'] == entry['id']:
                not_in_list = False
            else:
                not_in_list =  True
        if self._videos.empty:
            not_in_list = True
        if self._verbosity:
            print(f'not_in_list {not_in_list}')
        return not_in_list

    def get_video_list(self, num_videos_requested, max_length_seconds, buffer_len=30):
        '''
        Main driver function for TikTokTools. Returns a list of max length
         num_videos_requested tiktokapi videos (dict) from the TikTokAPI
         'Trending' category. The list will then be filtered to make sure each
         video is not over max_length_seconds.

        args:
            num_videos_requested (int):
                Number of videos to try to return based on length parameter
            max_length_seconds (int):
                Filter video list by maximum length. Will try to return a list
                of videos no longer than length_seconds
        kwargs:
            buffer_length (int): 
                number of unparsed videos to initially download
                This is a hotfix to solve getting unique tiktoks
        
        Returns:
            videos (list): 
                list of dictionary tiktok objects
        '''
        # TODO BUG every time a new video is requested, it always retrieves
        # the first video in a list somewhere that is always the same. Need
        videolist_raw = self._api.trending(buffer_len, custom_verifyFp="")
        # to retrieve unique video.
        # HOTFIX: Retrieve a list of 20, 30, 50 videos and parse through each
        # of those as the results.
        self._requested_length = max_length_seconds
        for video in videolist_raw:
            # TODO eventually implement where new UNIQUE video is retrieved until list
            # is full
            self._add_video(video)
            if len(self._videos.queue) >= num_videos_requested:
                return self._videos.queue

    def _add_video(self, video):
        '''
        Add new video to self.videos list
        '''
        not_in_list = self._check_video_not_in_list(video)
        is_shorter = self._check_video_shorter_than(video)
        added_video = None
        if (is_shorter and not_in_list): 
            self._videos.put(video)
            added_video = True
        else:
            added_video = False
        if self._verbosity:
            print(f'added_video {added_video}')
        return added_video

    def _get_video_by_keyword(self):
        '''
        Get video by keyword search
        '''
        raise NotImplementedError

    def get_video_author(self, tiktokobject):
        return tiktokobject['desc']

    def get_video_download_address(self, tiktokobject):
        return tiktokobject['video']['downloadAddr']

    def get_video_description(self, tiktokobject):
        return tiktokobject['author']['nickname']
