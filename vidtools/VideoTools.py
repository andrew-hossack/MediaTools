'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-05 21:39:13
 # @ Description: VideoTools Class File
 '''


import collections.abc
import os
import pprint
from queue import Queue
import requests
from vidtools.WorkspaceManager import ManagedWorkspace
import yaml


class VideoTools(ManagedWorkspace):
    '''
    VideoTools class for video postprocessing and configuration management.
    Video config can be managed with video.yaml found in the root directory
    '''
    def __init__(self, config_yaml='video.yaml'):
        '''
        Loads in video.yaml config settings
        kwargs:
            config_yaml (str):
                Name of configuration yaml file to load in from 
                Defaults to video.yaml
        '''
        super().__init__()
        self.config = {}
        self.managed_dir_path
        self._download_q = Queue()
        self._config_yaml_path = self.managed_dir_path.joinpath(config_yaml)
        self.cleanup()
        self._load_config()

    def video_downloader_from_url(self, download_url, title='video'):
        '''
        Download video from url to filepath to self.managed_dir_path
        title (str): optional title of download, do not include '.mp4'
            will append '_n' where n (int) repreents repeated filenames
        '''
        n = sum(
            1 for f in os.listdir(self.managed_dir_path) if os.path.isfile(
                os.path.join(self.managed_dir_path, f)))
        title = f'{title}_{n}'
        self._download_q.put(download_url)
        with requests.get(self._download_q.get(), allow_redirects=True) as req:
            with open(os.path.join(self.managed_dir_path, f'{title}.mp4'), 'wb') as file:
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
        self._update_config_recursive(self.config, updated_dict)

    def _update_config_recursive(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self._update_config_recursive(d.get(k, {}), v)
            else:
                d[k] = v
        with open(self._config_yaml_path, "w") as f:
            yaml.dump(d, f)
        return d

    def _load_config(self):
        '''
        Get config data from self.config_yaml file and update self
        '''
        self.config = self.load_yaml(self._config_yaml_path)
        self.title = self.config['video']['title']
        self.description = self.config['video']['description']
        self.author = self.config['video']['author']
        self.runtime = self.config['video']['playtime_min_seconds']
        self.tags = self.config['metadata']['tags']

    def pp_config(self):
        '''
        Pretty print config
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.config)

    def compile_all(self):
        '''
        Method to compile video data from self.managed_dir_path
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