'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-14 16:19:32
 '''


import json
import os
from pathlib import Path
import yaml


class ManagedWorkspace:
    '''
    Workspace manager baseclass to manage configurations and
     file settings. Also manages client secrets files and
     environment variables.
     '''

    def __init__(self, secrets_filepath, managed_path='dat'):
        '''
        args:
            secrets_filepath (str):
                Absolute filepath of secrets json file to load
        kwargs:
            managed_path (str):
                Managed directory name from root
                Defaults to /dat
        '''
        if secrets_filepath:
            self.secrets_path = Path(secrets_filepath)
        self.managed_dir_path = Path(__file__).parent.joinpath(managed_path)

    def cleanup(self):
        '''
        Remove all files from _managed_dir
        '''
        os.system(f'rm -rf {self.managed_dir_path}/*')

    def load_yaml(self, config_filepath):
        '''
        Loads in configuration yaml files
        args:
            config_filepath (str):
                Absolute filepath of config file to load
        Returns a yaml object
        '''
        with open(self._config_yaml_path) as config:
            config = yaml.load(config, Loader=yaml.FullLoader)
        return config

    def load_json(self, config_filepath):
        '''
        Loads in json or secrets files
        args:
            config_filepath (str):
                Absolute filepath of config file to load
        Returns a yaml object
        '''
        with open(self._config_yaml_path) as config:
            config = json.load(config)
        return config
