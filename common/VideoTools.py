'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-05 21:39:13
 # @ Description: VideoTools Class File
 '''

import os
from pathlib import Path
import yaml

class VideoTools():
    '''
    VideoTools class for video postprocessing
    '''
    def __init__(self):
        '''
        Loads in video.yaml config settings
        '''
        self._config = {}
        self._downloads_dir = Path(f'{Path(os.path.join(os.path.dirname(__file__))).parent}/dat')
        CONFIG_YAML = Path(os.path.join(os.path.dirname(__file__))).parent.joinpath('video.yaml')
        with open(CONFIG_YAML) as config:
            self._config = yaml.load(config, Loader=yaml.FullLoader)
        self.title = self._config['video']['title']
        self.description = self._config['video']['description']
        self.author = self._config['video']['author']
        self._cleanup_downloads_dir()

    def video_downloader_from_url(self, download_url):
        '''
        Download video from url to filepath
        '''
        raise NotImplementedError

    def _cleanup_downloads_dir(self):
        '''
        Remove all files from _downloads_dir
        '''
        os.system(f'rm -rf {self._downloads_dir}/*')