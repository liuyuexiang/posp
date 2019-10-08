import yaml
import os

from log import PlatformLog


class SysConfig(PlatformLog):
    # config = {}

    def __init__(self, default_path="sys_config.yaml"):
        super(SysConfig, self).__init__()
        path = default_path

        if os.path.exists(path):
            with open(path, "r") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
                # print(self.config['queue']['queuename'])


