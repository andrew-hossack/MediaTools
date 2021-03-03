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
        self._verbosity = verbosity

    def _check_video_shorter_than(self, video_entry):
        '''
        Returns boolean if video is less than given length
        '''
        res = video_entry['video']['duration'] < self.requested_length
        if self._verbosity:
            print("Video shorter than {self.requested_length}: {res}")
        return res

    def _check_video_not_in_list(self, video):
        '''
        Returns boolean if video being checked is in self.videos
        '''
        for entry in self.videos:
            if video == entry:
                if self._verbosity:
                    print("Video in list, retrieving new one...")
                return False
        return True

    def get_video_list(self, num_videos_requested, length_seconds):
        '''
        Return video list
        videos (list): list of dictionary tiktok objects
        '''
        self.requested_length = length_seconds
        while len(self.videos) < num_videos_requested:
            self._add_video()
        return self.videos

    def _add_video(self, ):
        video = self.api.trending(count=1, custom_verifyFp="")[0]
        if self._check_video_shorter_than(video) and self._check_video_not_in_list(video): 
            self.videos.append(video)
            if self._verbosity:
                print("Added new video")
            return True
        else:
            return False