import yaml


class YamlLoader():
    @classmethod
    def from_yaml(cls, file):
        with open(file, 'r') as f:
            return cls.from_yaml_string(f.read())


    @classmethod
    def from_yaml_string(cls, yaml_string):
        return cls.from_dict(yaml.load(yaml_string))
