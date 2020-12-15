import yaml


class Cfg(dict):
    def __init__(self, config_dict):
        super(Cfg, self).__init__(**config_dict)
        self.__dict__ = self

    @staticmethod
    def load_config_from_file(fn):
        with open(fn, encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return Cfg(config)
