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

    # @staticmethod
    # def load_config_from_file(fname=None):
    #     with open("./tmp/base.yml", encoding='utf-8') as f:
    #         base_config = yaml.safe_load(f)
    #     with open("./tmp/vgg-transformer.yml", encoding='utf-8') as f:
    #         config = yaml.safe_load(f)
    #     base_config.update(config)
    #     return Cfg(base_config)
    #
    # def save(self, fname):
    #     with open(fname, 'w') as f:
    #         yaml.dump(dict(self), f, default_flow_style=False, allow_unicode=True)
