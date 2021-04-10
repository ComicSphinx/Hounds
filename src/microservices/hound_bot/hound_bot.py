# @Author: Daniil Maslov (ComicSphinx)

from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests, json, logging, time
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level = logging.INFO)

logger = logging.getLogger(__name__)

def handler_start(update, context):
    print("/start")
    update.message.reply_text("Hello!")
    update.message.reply_text("Use /get_cost to get cost")
    update.message.reply_text("Use /get_income to get income")
    update.message.reply_text("Use /get_auto_info")

def handler_get_cost(update: Update, _: CallbackContext) -> None:
    data = requests.get("http://127.0.0.1:5000/get/id")
    data = data.json()
    update.message.reply_text("Investment portfolio value: " + str(data['cost']) + "Rub")

def handler_get_income(update: Update, _: CallbackContext) -> None:
    data = requests.get("http://127.0.0.1:5000/get/id")
    data = data.json()
    update.message.reply_text("Investment portfolio income: " + str(data['income']) + "Rub")

def handler_get_auto_info(update: Update, _: CallbackContext) -> None:
    print("/get_auto_info")
    goal_income = 300
    # wait 60 minutes
    time_wait = 60 * 60
    # wait 15 seconds
    # time_wait = 15

    while(True):
        time.sleep(time_wait)
        data = requests.get("http://127.0.0.1:5000/get/id")
        data = data.json()

        print("goal_income:", goal_income)
        print("float(data['income'])", float(data['income']))
        if (goal_income <= float(data['income'])):
            update.message.reply_text("Congratulations! Goal achieved! Your income:" + str(data['income']) + "Rub")

# def handler_set_goal(update: Update, context: CallbackContext) -> None:
#         try:
#             # args[0] should contain the time for the timer in seconds
#             due = int(context.args[0])
#             if due < 0:
#                 update.message.reply_text('Sorry we can not go back to future!')
#                 return

#             context.job_queue.run_once(set_goal, due)

#             text = 'Goal successfully updated'
#             update.message.reply_text(text)

#         except (IndexError, ValueError):
#             update.message.reply_text('Usage: /set_goal <value>')

# def set_goal(number):
#     goal_income = number

def main():
    updater = Updater(token = 'token', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handler_start))
    dispatcher.add_handler(CommandHandler("get_cost", handler_get_cost))
    dispatcher.add_handler(CommandHandler("get_income", handler_get_income))
    dispatcher.add_handler(CommandHandler("get_auto_info", handler_get_auto_info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()