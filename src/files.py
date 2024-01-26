from typing import Dict
import json
import os

class Files:
    _credentials_filepath: str = r'Credentials\\Credentials.json'
    _common_messages_filepath: str = r'Data\\messages.json'
    _menus_filepath: str = r'Data\\menus.json'

    _json_credentials: Dict[str, str] = None
    _bot_token: str = ''

    _common_messages: Dict[str, str] = None

    _menus: Dict[str, str] = None

    def open_files(self) -> None:
        if (os.path.isfile(self._credentials_filepath)):
            with open(self._credentials_filepath, 'r') as fin:
                self._json_credentials = json.load(fin)
                self._bot_token = self._json_credentials['BOT_TOKEN']
                self._pantry_token = self._json_credentials['PANTRY_TOKEN']

        if (os.path.isfile(self._common_messages_filepath)):
            with open(self._common_messages_filepath, 'r') as fin:
                self._common_messages = json.load(fin)
        else:
            print(f"NO messages found at {self._common_messages_filepath}")

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
    def help_message(self) -> str:
        return "\n".join(self._common_messages.values())

    @property
    def menu_message(self) -> str:
        return self._common_messages.get('menu', '')

    @property
    def menus(self) -> Dict[str, str]:
        return self._menus