from os import stat
import telegram
import subprocess
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import logging

def is_member(bot, chat_id, user_id):
    chat_member = bot.get_chat_member(chat_id, user_id)
    # print(chat_member.status)
    if chat_member.status == "member":
        return True
    else:
        return False

def is_admin(bot, chat_id, user_id):
    chat_member = bot.get_chat_member(chat_id, user_id)
    # print(chat_member)
    if chat_member.status == "creator" or chat_member.status == "administrator":
        return True
    else:
        return False

def get_thread_url(chat_id, message_id):
    return 't.me/c/'+str(chat_id).replace('-100', '')+'/'+str(message_id)+'?thread='+str(message_id)

def entry(bot, update):
    try:
        # res = bot.send_message(chat_id="-1001164870268", text=json.dumps(update.to_dict(), indent=2))
        print(json.dumps(update.to_dict(), indent=2))
        pass
    except Exception as e:
        logging.error(e)
        bot.send_message(chat_id="-1001164870268", text=str(e))
        pass
    if update.message and update.message.text and not update.message.reply_to_message:
        if is_member(bot,update.message.chat.id, update.message.from_user.id):
            thread_url=get_thread_url(update.message.chat.id, update.message.message_id)
            keyboard = [
                [InlineKeyboardButton("Resolve", callback_data='resolve'),
                InlineKeyboardButton("Open Thread", url=thread_url)
                ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=update.message.chat.id,
                reply_to_message_id=update.message.message_id,
                text="#open",
                reply_markup=reply_markup)
    elif update.callback_query:
        if is_admin(bot,update.callback_query.message.chat.id, update.callback_query.from_user.id):
            thread_url = get_thread_url(
                update.callback_query.message.chat.id, 
                update.callback_query.message.reply_to_message.message_id)
            keyboard = [[InlineKeyboardButton("Open Thread", url=thread_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.editMessageText(
                chat_id=update.callback_query.message.chat.id,
                message_id=update.callback_query.message.message_id, text="#resolved",
                reply_markup=reply_markup)
        else:
            bot.answer_callback_query(callback_query_id=update.callback_query.id, text="Only Admins are allowed to Resolve items", show_alert=True)
