import json
import os
import telebot
from utils import parse_menu


if __name__ == "__main__":
    BOT_TOKEN = json.load(open("Credentials\\Credentials.json"))["BOT-TOKEN"]

    bot = telebot.TeleBot(BOT_TOKEN)
    bot.infinity_polling()

@bot.message_handler(commands=['menu'])
def get_menu(message):
    text = message.text
    sender = message.chat.id
    menus = json.load(open("Data\\menus.json"))
        
    
    bot.reply_to(message, "Menu saved")
    
@bot.message_handler(commands=['help'])
def get_menu(message):
    help_message = json.load(open("Data\\messagges.json"))
    messages = "\n".join([message for message in help_message.values])
    
    bot.reply_to(message, messages)