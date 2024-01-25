import json
import os
import telebot
from telebot import types
from src import utils as uts
from typing import Dict


class Files:
    _credentials_filepath: str = r'Credentials\Credentials.json'
    _common_messages_filepath: str = r'Data\messages.json'
    _menus_filepath: str = r'Data\menus.json'

    _json_credentials: Dict[str, str] = None
    _bot_token: str = ''

    _common_messages: Dict[str, str] = None

    _menus: Dict[str, str] = None

    def open_files(self) -> None:
        if (os.path.isfile(self._credentials_filepath)):
            with open(self._credentials_filepath, 'r') as fin:
                self._json_credentials = json.load(fin)
                self._bot_token = self._json_credentials['BOT_TOKEN']

        if (os.path.isfile(self._common_messages)):
            with open(self._common_messages_filepath, 'r') as fin:
                self._common_messages = json.load(fin)

        if (os.path.isfile(self._menus_filepath)):
            with open(self._menus_filepath, 'r') as fin:
                self._menus = json.load(fin)

    def save_menus() -> None:
        with open(self._menus_filepath, 'w') as fout:
            json.dump(self._menus, fout)

    @property
    def BOT_TOKEN(self) -> str:
        return self._bot_token

    @property
    def help_message(self) -> str:
        return self._common_messages.get('help', '')

    @property
    def menu_message(self) -> str:
        return self._common_messages.get('menu', '')

    @property
    def menus(self) -> Dict[str, str]:
        return self._menus


if __name__ == "__main__":

    files = Files()
    files.open_files()

    bot = telebot.TeleBot(files.BOT_TOKEN)

    print("Start the bot polling...")

    @bot.message_handler(commands=['start', 'help'])
    def help(message):
        bot.reply_to(message, files.help_message)

    @bot.message_handler(commands=['menu'])
    def get_menu(message):
        text = message.text
        sender = message.chat.id
        menus = files.menus

        menu = uts.parse_menu(text)
        menus.update({sender: menu})

        files.save_menus()

        bot.reply_to(message, "Menu saved")

    @bot.message_handler(commands=['riassunto'])
    def help(message):
        menu_code = message.text.strip()
        sender = message.chat.id

        menu_recap = uts.recap(sender, menu_code)

        bot.reply_to(message, menu_recap)

    @bot.message_handler(commands=['test_menu'])
    def test_menu(message):
        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button = types.KeyboardButton("Place order", web_app=types.WebAppInfo(
            'https://96Octavian.github.io/menu_webapp/?code=test_menu'))

        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.add(button)

        bot.reply_to(
            message, text='Open the keyboard and press to place your order', reply_markup=kb)

    @bot.message_handler(content_types=['web_app_data'])
    def handle_any(message):
        hideBoard = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, message.web_app_data.data, reply_markup=hideBoard)

    bot.infinity_polling()
