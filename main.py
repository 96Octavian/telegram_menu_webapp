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
        bot.reply_to(message, files.help_message)

    @bot.message_handler(commands=['menu'])
    def command_menu(message):
        text = message.text

        menus = files.menus
        menu = uts.parse_menu(text)
        menu_code = uts.generate_code(menus.keys())
        # menus.update({menu_code: menu})   # Updating a dict is a cotly operation we can avoid in this case; doing it before checking upload_results also means we're already updating files.menus as they're referencing the same object

        upload_result = uts.upload_to_pantry(menu_code, menu)

        if upload_result:
            # files.menus = menus   # The following line is already enough (menus and files.menus are the same object)
            menus[menu_code] = menu
            files.save_menus()
            bot.reply_to(message, f"Menu saved with code: {menu_code}")
        else:
            bot.reply_to(message, f"Error uploading menu")

    @bot.message_handler(commands=['order'])
    def command_order(message):
        menu_code = message.text.split(" ")[-1].strip()

        button = types.KeyboardButton(
            "Place order",
            web_app=types.WebAppInfo(
                f'https://96Octavian.github.io/menu_webapp/?code={menu_code}'
            )
        )
        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.add(button)

        bot.reply_to(
            message,
            text='Open the keyboard and press to place your order',
            reply_markup=kb
        )

    @bot.message_handler(commands=['summary'])
    def command_summary(message):
        menu_code = message.text.split(" ")[-1].strip()
        sender = message.chat.id

        menu_recap = uts.recap(sender, menu_code)

        bot.reply_to(message, menu_recap)

    @bot.message_handler(commands=['open'])
    def command_open(message):
        menu_code = message.text.split(" ")[-1].strip()
        menus = files.menus

        reply = ""
        try:
            if menus[menu_code]["creator_id"] == message.chat.id:
                open_result = uts.upload_to_pantry(menu_code, menus[menu_code])
                if open_result:
                    menus[menu_code]["active"] = True
                    # files.menus = menus   # Not needed -menus is a reference to files.menus, it's the same dictionary
                    files.save_menus()
                    reply = f"Menu {menu_code} open"
                else:
                    reply = f"Unable to open menu {menu_code}"
            else:
                reply = f"You're not the creator of the menu! Go away!"
        except:
            reply = f"Menu code not found!"

        bot.reply_to(message, reply)

    @bot.message_handler(commands=['close'])
    def command_close(message):
        menu_code = message.text.split(" ")[-1].strip()
        menus = files.menus

        reply = ""
        try:
            if menus[menu_code]["creator_id"] == message.chat.id:
                closure = uts.delete_from_pantry(menu_code)
                if closure:
                    menus[menu_code]["active"] = False
                    # files.menus = menus   # Not needed -menus is a reference to files.menus, it's the same dictionary
                    files.save_menus()
                    reply = f"Menu {menu_code} closed"
                else:
                    reply = f"Unable to close menu {menu_code}"
            else:
                reply = f"You're not the creator of the menu! Go away!"
        except:
            reply = f"Menu code not found!"

        bot.reply_to(message, reply)

    @bot.message_handler(content_types=['web_app_data'])
    def handle_web_app_data(message):
        hideBoard = types.ReplyKeyboardRemove()
        print(message.web_app_data.data)
        bot.send_message(
            message.chat.id,
            message.web_app_data.data,
            reply_markup=hideBoard
        )

    bot.infinity_polling()
