'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-05 21:39:13
 # @ Description: VideoTools Class File
 '''

import os
from pathlib import Path
import pprint
from queue import Queue
import requests
from time import sleep, time
import yaml

class VideoTools():
    '''
    VideoTools class for video postprocessing
    '''
    def __init__(self, config_yaml='video.yaml', download_dir='dat/temp'):
        '''
        Loads in video.yaml config settings
        '''
        self._config = {}
        self._download_q = Queue()
        self._downloads_dir = Path(f'{Path(os.path.join(os.path.dirname(__file__))).parent}/{download_dir}')
        self._config_yaml_path = Path(os.path.join(os.path.dirname(__file__))).parent.joinpath(config_yaml)
        self._cleanup_downloads_dir()
        self.get_config_data_from_yaml()

    def video_downloader_from_url(self, download_url, title='video'):
        '''
        Download video from url to filepath to self._downloads_dir
        title (str): optional title of download
            will append '_n' where n (int) repreents repeated filenames
        '''
        n = sum(1 for f in os.listdir(self._downloads_dir) if os.path.isfile(os.path.join(self._downloads_dir, f)))
        title = f'{title}_{n}'
        self._download_q.put(download_url)
        with requests.get(self._download_q.get(), allow_redirects=True) as req:
            with open(f'{self._downloads_dir}/{title}.mp4', 'wb') as file:
                file.write(req.content)

    def _cleanup_downloads_dir(self):
        '''
        Remove all files from _downloads_dir
        '''
        os.system(f'rm -rf {self._downloads_dir}/*')

    def get_config_data_from_yaml(self):
        '''
        Get config data from self._config_yaml file and update self
        '''
        with open(self._config_yaml_path) as config:
            self._config = yaml.load(config, Loader=yaml.FullLoader)

        # TODO consider not setting self.XYZ and rather just reference the yaml
        self.title = self._config['video']['title']
        self.description = self._config['video']['description']
        self.author = self._config['video']['author']
        self.runtime = self._config['video']['playtime_min_seconds']
        self.metadata = self._config['metadata']['tags']

    def get_config(self):
        '''
        Returns the config yaml file video.yaml
        '''
        return self._config

    def pp_config(self):
        '''
        Pretty print config
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self._config)

    def compile_all(self):
        '''
        Method to compile video data from self._downloads_dir
        Features to consider adding:
            - Intro and outtro video
            - Resolution
            - Background audio
        '''
        raise NotImplementedError


if __name__ == '__main__':
    vt = VideoTools()
    print('~~~~ VideoTools ~~~~')
    vt.pp_config()