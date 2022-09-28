# -*- coding:utf-8 -*-
import os
import pathlib
import yaml
import typing as ty


class SettingsBase(object):

    BASE_DIR = pathlib.Path(__file__).parent.parent
    
    def configure(self, config_file: str) -> None:
        if not config_file:
            return

        with open(config_file, 'r', encoding='utf-8') as f:
            __config = yaml.load(f, Loader=yaml.CLoader)

        for k, v in __config.items():
            setattr(self, k.upper(), v)

    # def __getattribute__(self, __name: str) -> ty.Any:
    #     globs = super().__getattribute__('__dict__')
    #     v = globs.get(__name)
    #     if v:
    #         return v
    #
    #     v = os.environ.get(__name)
    #     if not v:
    #         return None
    #
    #     return v


class Settings(SettingsBase):
    FLOMO_SDK = None
    FLOMO_API_KEY = None

    IMAP_SERVER = ''
    IMAP_PORT = 993
    IMAP_USER = ''
    IMAP_PASSWORD = ''
    IMAP_MAILBOX = 'INBOX'


settings = Settings()
