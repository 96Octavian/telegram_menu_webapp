import telebot
from telebot import types
from src import utils as uts
from src import files as fls


if __name__ == "__main__":

    files = fls.Files()
    files.open_files()

    bot = telebot.TeleBot(files.BOT_TOKEN)

    print("Start the bot polling...")

    @bot.message_handler(commands=['start', 'help'])
    def help(message):
        # bot.reply_to(message, files.help_message)
        bot.reply_to(message, message.chat.id)

    @bot.message_handler(commands=['menu'])
    def create_menu(message):
        text = message.text
        
        menus = files.menus
        menu = uts.parse_menu(text)
        menu_code = uts.generate_code(menus.keys())
        menus.update({menu_code: menu})
       
        upload_result = uts.load_menu(menu_code, menu)
    
        if upload_result:
            files.menus = menus
            files.save_menus()
            bot.reply_to(message, f"Menu saved with code: {menu_code}")
        else:
            bot.reply_to(message, f"Errore nel caricamento del menù")

    # TODO Add order function @LOCKE
    @bot.message_handler(commands=['ordina'])
    def create_menu(message):
        pass
    
    @bot.message_handler(commands=['riassunto'])
    def help(message):
        menu_code = message.text.split(" ")[-1].strip()
        sender = message.chat.id

        menu_recap = uts.recap(sender, menu_code)

        bot.reply_to(message, menu_recap)

    @bot.message_handler(commands=['test_menu'])
    def test_menu(message):
        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        
        menu_code = message.text.split(" ")[-1].strip()
        
        button = types.KeyboardButton("Place order", web_app=types.WebAppInfo(
            'https://96Octavian.github.io/menu_webapp/?code={menu_code}'))

        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.add(button)

        bot.reply_to(
            message, text='Open the keyboard and press to place your order', reply_markup=kb)

    @bot.message_handler(commands=['apri'])
    def open_menu(message):
        menu_code = message.text.split(" ")[-1].strip()
        menus = files.menus
        
        reply = ""
        try:
            if menus[menu_code]["Creator_ID"] == message.chat.id:
                menus[menu_code]["Active"] = False
                open_result = uts.load_menu(menu_code, menus[menu_code])
                if open_result:
                    files.menus = menus
                    files.save_menus()
                    reply = f"{menu_code} menu closed"
                else:
                    reply = f"Impossible close menu {menu_code}"
            else:
                reply = f"You're not the creator of the menu! Go away!"
        except:
            reply = f"Menu code not found!"
        
        bot.reply_to(message, reply)

    @bot.message_handler(commands=['chiudi'])
    def close_menu(message):
        menu_code = message.text.split(" ")[-1].strip()
        menus = files.menus
        
        reply = ""
        try:
            if menus[menu_code]["Creator_ID"] == message.chat.id:
                closure = uts.close_menu(menu_code)
                if closure:
                    menus[menu_code]["Active"] = False
                    files.menus = menus
                    files.save_menus()
                    reply = f"{menu_code} menu close"
                else:
                    reply = f"Impossible close menu {menu_code}"
            else:
                reply = f"You're not the creator of the menu! Go away!"
        except:
            reply = f"Menu code not found!"
        
        bot.reply_to(message, reply)

    @bot.message_handler(content_types=['web_app_data'])
    def handle_any(message):
        hideBoard = types.ReplyKeyboardRemove()
        print(message.web_app_data.data)
        bot.send_message(
            message.chat.id, message.web_app_data.data, reply_markup=hideBoard)

    bot.infinity_polling()
