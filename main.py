import telebot
from telebot import types
from src import utils as uts
from src import files as fls
import json


if __name__ == "__main__":

    files = fls.Files()
    files.open_files()

    bot = telebot.TeleBot(files.BOT_TOKEN)

    print("Start the bot polling...")

    @bot.message_handler(commands=['start', 'help'])
    def help(message):
        reply = (
            files
            .common_messages
            .help_message
            .get(message.from_user.language_code)
        )
        bot.reply_to(
            message,
            reply,
            parse_mode='HTML'
        )

    @bot.message_handler(commands=['menu'])
    def command_menu(message):
        lang = message.from_user.language_code
        text = message.text

        menu = uts.parse_menu(text)
        sender = message.from_user.id
        menu['creator_id'] = str(sender)

        menus = files.menus
        menu_code = uts.generate_code(menus.keys())
        # menus.update({menu_code: menu})   # Updating a dict is a cotly operation we can avoid in this case; doing it before checking upload_results also means we're already updating files.menus as they're referencing the same object

        upload_result = uts.upload_to_pantry(menu_code, menu)

        if upload_result:
            # files.menus = menus   # The following line is already enough (menus and files.menus are the same object)
            menus[menu_code] = menu
            files.save_menus()
            reply = (
                files
                .common_messages
                .menu_saved_with_code
                .get(lang)
                .format(menu_code=menu_code)
            )
            bot.reply_to(message, reply,parse_mode='HTML')
        else:
            reply = (
                files
                .common_messages
                .upload_error
                .get(lang)
            )
            bot.reply_to(message, reply)

    @bot.message_handler(commands=['order'])
    def command_order(message):
        menu_code = message.text.split(" ")[-1].strip()

        button = types.KeyboardButton(
            files.common_messages.place_order.get(
                message.from_user.language_code),
            web_app=types.WebAppInfo(
                f'https://96Octavian.github.io/menu_webapp/?code={menu_code}'
            )
        )
        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.add(button)

        bot.reply_to(
            message,
            text=files.common_messages.place_order_message.get(
                message.from_user.language_code),
            reply_markup=kb
        )

    @bot.message_handler(commands=['revoke_order'])
    def command_revoke(message):
        lang = message.from_user.language_code
        order = json.loads(message.web_app_data.data)
        menu_code = order['code']
        menu = files.menus.get(menu_code, None)
        if not menu:
            bot.reply_to(
                message,
                files.common_messages.menu_not_found.get(lang)
            )
            return

        order = menu['orders'].pop(message.from_user.id, None)
        if not order:
            reply = (
                files
                .common_messages
                .order_not_found
                .get(lang)
            )
            bot.reply_to(message, reply)
            return

        files.save_menus()
        reply = (
            files
            .common_messages
            .order_revoked
            .get(lang)
        )
        bot.reply_to(message, reply)

    @bot.message_handler(commands=['summary'])
    def command_summary(message):
        lang = message.from_user.language_code
        menu_code = message.text.split(" ")[-1].strip()
        menu = files.menus.get(menu_code, None)
        if not menu:
            bot.reply_to(
                message,
                files.common_messages.menu_not_found.get(lang)
            )
            return

        sender = message.from_user.id
        if menu['creator_id'] != str(sender):
            reply = (
                files
                .common_messages
                .not_the_creator
                .get(lang)
            )
            bot.reply_to(message, reply)
            return

        menu_message = uts.recap(menu)
        
        bot.reply_to(message, menu_message)

    @bot.message_handler(commands=['open'])
    def command_open(message):
        menu_code = message.text.split(" ")[-1].strip()
        menus = files.menus
        lang = message.from_user.language_code

        reply = ""
        try:
            if menus[menu_code]["creator_id"] == str(message.chat.id):
                open_result = uts.upload_to_pantry(menu_code, menus[menu_code])
                if open_result:
                    menus[menu_code]["active"] = True
                    # files.menus = menus   # Not needed -menus is a reference to files.menus, it's the same dictionary
                    files.save_menus()
                    reply = (
                        files
                        .common_messages
                        .menu_open_with_code
                        .get(lang)
                        .format(menu_code=menu_code)
                    )
                else:
                    reply = (
                        files
                        .common_messages
                        .menu_open_with_code_error
                        .get(lang)
                        .format(menu_code=menu_code)
                    )
            else:
                reply = (
                    files
                    .common_messages
                    .not_the_creator
                    .get(lang)
                )
        except:
            reply = (
                files
                .common_messages
                .menu_not_found
                .get(lang)
            )

        bot.reply_to(message, reply)

    @bot.message_handler(commands=['close'])
    def command_close(message):
        menu_code = message.text.split(" ")[-1].strip()
        menus = files.menus
        lang = message.from_user.language_code

        reply = ""
        try:
            if menus[menu_code]["creator_id"] == str(message.chat.id):
                closure = uts.delete_from_pantry(menu_code)
                if closure:
                    menus[menu_code]["active"] = False
                    # files.menus = menus   # Not needed -menus is a reference to files.menus, it's the same dictionary
                    files.save_menus()
                    reply = (
                        files
                        .common_messages
                        .menu_close_with_code
                        .get(lang)
                        .format(menu_code=menu_code)
                    )
                else:
                    reply = (
                        files
                        .common_messages
                        .menu_open_with_code_error
                        .get(lang)
                        .format(menu_code=menu_code)
                    )
            else:
                reply = files.common_messages.not_the_creator.get(lang)
        except:
            reply = files.common_messages.menu_not_found.get(lang)

        bot.reply_to(message, reply)

    @bot.message_handler(content_types=['web_app_data'])
    def handle_web_app_data(message):
        lang = message.from_user.language_code
        order = json.loads(message.web_app_data.data)
        menu_code = order['code']
        menu = files.menus.get(menu_code, None)
        if not menu:
            bot.send_message(
                message.chat.id,
                files.common_messages.menu_not_found.get(lang)
            )
            return

        menu['orders'][message.from_user.id] = order['choices']
        files.save_menus()

        hideBoard = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            files.common_messages.order_received.get(lang),
            reply_markup=hideBoard
        )
        menu_message = ""
        for course, meals in order['choices'].items():
            menu_message += f"{course}\n"
            for meal, amount in meals.items():
                menu_message += f"\t{amount}x {meal}\n"
        bot.send_message(message.chat_id, menu_message)

    bot.infinity_polling()
