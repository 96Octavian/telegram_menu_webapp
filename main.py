import json
import os
import telebot
from telebot import types
from src import utils as uts


if __name__ == "__main__":
    BOT_TOKEN = json.load(open("Credentials\\Credentials.json"))["BOT-TOKEN"]
    bot = telebot.TeleBot(BOT_TOKEN)
    
    print("Start the bot polling...")
    

    @bot.message_handler(commands=['start','help'])
    def help(message):
        help_message = json.load(open("Data\\messagges.json"))
        messages = "\n".join([message for message in help_message.values()])
        
        bot.reply_to(message, messages)

    @bot.message_handler(commands=['menu'])
    def get_menu(message):
        text = message.text
        sender = message.chat.id
        menus = json.load(open("Data\\menus.json"))
        
        menu = uts.parse_menu(text)
        menus.update({sender : menu})
        
        # Save the menu
        with open(".//Data//menus.json", "w") as f:
            json.dump(menus, f)
        
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
        button = types.KeyboardButton("Place order", web_app=types.WebAppInfo('https://96Octavian.github.io/menu_webapp/?code=test_menu'))

        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.add(button)

        bot.reply_to(message, text='Open the keyboard and press to place your order', reply_markup=kb)
    
    @bot.message_handler(content_types=['web_app_data'])
    def handle_any(message):
        hideBoard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message.web_app_data.data, reply_markup=hideBoard)

    bot.infinity_polling()
    
    