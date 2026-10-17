import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Type

import appdirs
import yaml

project_dir = Path(__file__).resolve().parent.parent
app_dir = Path(sys._MEIPASS) if getattr(
    sys, 'frozen', False
) else Path(__file__).parent


@dataclass
class Config(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Config"

    lang: str = 'en'


class Resources:
    app_name = "Archmaster Chess"
    author = "Archmaster"

    def __init__(self):
        if (project_dir / '.git').is_dir():
            self.user_dir = Path('./user_data')
        else:
            self.user_dir = Path(appdirs.user_data_dir(
                self.app_name, self.author))

        self.user_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.user_dir / 'config.yaml'
        self.load_config()

    def load_config(self):
        self.config = self.load_yaml(self.config_file, Config)

    def save_config(self):
        self.dump_yaml(self.config_file, self.config)

    def load_yaml(self, file, data_class: Type[yaml.YAMLObject]):
        if file.exists():
            with open(file, 'r', encoding='utf-8') as stream:
                return yaml.load(stream, data_class.yaml_loader)
        data = data_class()
        self.dump_yaml(file, data)
        return data

    def dump_yaml(self, file, data: yaml.YAMLObject):
        with open(file, 'w', encoding='utf-8') as stream:
            yaml.dump(data, stream)

    @property
    def font_dir(self):
        return app_dir / 'fonts'

    @property
    def pieces_dir(self):
        return app_dir / 'pieces'

    @property
    def qml_dir(self):
        return app_dir / 'qml'


resources = Resources()
