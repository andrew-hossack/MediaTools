'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-05 21:39:13
 # @ Description: VideoTools Class File
 '''


import collections.abc
import os
from pathlib import Path
import pprint
from queue import Queue
import requests
import yaml


class VideoTools:
    '''
    VideoTools class for video postprocessing and configuration management.
    Video config can be managed with video.yaml found in the root directory
    '''
    def __init__(self, config_yaml='video.yaml', download_dir='dat/temp'):
        '''
        Loads in video.yaml config settings
        '''
        self._config = {}
        self._download_q = Queue()
        self._downloads_dir = Path(__file__).parent.joinpath(download_dir)
        self._config_yaml_path = Path(__file__).parent.joinpath(config_yaml)
        self._cleanup_downloads_dir()
        self._load_config()

    def video_downloader_from_url(self, download_url, title='video'):
        '''
        Download video from url to filepath to self._downloads_dir
        title (str): optional title of download, do not include '.mp4'
            will append '_n' where n (int) repreents repeated filenames
        '''
        n = sum(
            1 for f in os.listdir(self._downloads_dir) if os.path.isfile(
                os.path.join(self._downloads_dir, f)))
        title = f'{title}_{n}'
        self._download_q.put(download_url)
        with requests.get(self._download_q.get(), allow_redirects=True) as req:
            with open(os.path.join(self._downloads_dir, f'{title}.mp4'), 'wb') as file:
                file.write(req.content)

    def update_config(self, updated_dict):
        '''
        Update config file
        args:
            updated_dict (dict):
                Dictionary following video.yaml structure
        Example:
            updated_dict = {
                'video': {
                    'title':'Test Title Goes Here'
                    }
                }
            update_config(updated_dict)
        '''
        self._update_config_recursive(self._config, updated_dict)

    def _update_config_recursive(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self._update_config_recursive(d.get(k, {}), v)
            else:
                d[k] = v
        with open(self._config_yaml_path, "w") as f:
            yaml.dump(d, f)
        return d

    def _cleanup_downloads_dir(self):
        '''
        Remove all files from _downloads_dir
        '''
        os.system(f'rm -rf {self._downloads_dir}/*')

    def _load_config(self):
        '''
        Get config data from self._config_yaml file and update self
        '''
        with open(self._config_yaml_path) as config:
            self._config = yaml.load(config, Loader=yaml.FullLoader)
        self.title = self._config['video']['title']
        self.description = self._config['video']['description']
        self.author = self._config['video']['author']
        self.runtime = self._config['video']['playtime_min_seconds']
        self.tags = self._config['metadata']['tags']

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