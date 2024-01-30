from typing import Dict
import json
import os


MenuOrder = dict[str, dict[str, int]]   # {course: {dish: amount}}
Menu = dict[str, int | str | MenuOrder | dict[int, MenuOrder]]


class MultiLanguageMessage:
    _description: str = ""
    _message: dict[str, str] = {}

    def __init__(self, description: str, message: dict[str, str]):
        self._description = description
        self._message = dict(message)

    @property
    def description(self) -> str:
        return self._description

    def get(self, language='en'):
        return self._message.get(language if language else "en", self.description)


class CommonMessages:
    def __init__(self, messages: dict[str, dict[str, str]]):
        # if 'upload_failed' in messages:
        #     self._upload_failed = MultiLanguageMessage(messages['upload_failed'])
        # if 'help_message' in messages:
        #     self._upload_failed = MultiLanguageMessage(messages['help_message'])
        for key, value in messages.items():
            mm = MultiLanguageMessage(key, value)
            self.__setattr__(mm.description, mm)


class Files:
    _credentials_filepath: str = r'Credentials\\Credentials.json'
    _common_messages_filepath: str = r'Data\\messages.json'
    _menus_filepath: str = r'Data\\menus.json'

    _bot_token: str = ''

    _common_messages: CommonMessages = None

    _menus: Dict[str, str] = None

    def open_files(self) -> None:
        if (os.path.isfile(self._credentials_filepath)):
            with open(self._credentials_filepath, 'r') as fin:
                credentials = json.load(fin)
            self._bot_token = credentials['BOT_TOKEN']
            self._pantry_token = credentials['PANTRY_TOKEN']

        if (os.path.isfile(self._common_messages_filepath)):
            with open(self._common_messages_filepath, 'r') as fin:
                common_messages_dict = json.load(fin)
            cm = CommonMessages(common_messages_dict)
            self._common_messages = cm
        else:
            print(f"No messages found at {self._common_messages_filepath}")

        if (os.path.isfile(self._menus_filepath)):
            with open(self._menus_filepath, 'r') as fin:
                self._menus = json.load(fin)

    def save_menus(self) -> None:
        with open(self._menus_filepath, 'w') as fout:
            json.dump(self._menus, fout)

    @property
    def BOT_TOKEN(self) -> str:
        return self._bot_token

    @property
    def PANTRY_TOKEN(self) -> str:
        return self._pantry_token

    @property
    def common_messages(self) -> CommonMessages:
        return self._common_messages

    @property
    def menus(self) -> Dict[str, str]:
        return self._menus
