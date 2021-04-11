# @Author: Daniil Maslov (ComicSphinx)

import requests, json, logging, time, schedule
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from multiprocessing.pool import ThreadPool

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level = logging.INFO)

logger = logging.getLogger(__name__)

def handler_start(update, context):
    print(update.effective_chat.id, ":", "was connected and used /start")

    update.message.reply_text("Hello!")
    update.message.reply_text("Use /get_cost to get cost")
    update.message.reply_text("Use /get_income to get income")
    update.message.reply_text("Use /get_auto_info")

def get_data():
    data = requests.get("http://127.0.0.1:5000/get/id")
    data = data.json()
    return data

def handler_get_cost(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat.id, ":", "/get_cost")
    data = get_data()
    update.message.reply_text("Investment portfolio value: " + str(data['cost']) + "Rub")

def handler_get_income(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat.id, ":", "/get_income")
    data = get_data()
    update.message.reply_text("Investment portfolio income: " + str(data['income']) + "Rub")

def handler_get_auto_info(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat.id, ":", "/get_auto_info")
    # TODO: В какой-то момент этот поток нужно убивать
    pool = ThreadPool(processes=1)
    get_parse_data = pool.apply_async(income_scheduler, args=(context, update))

def income_scheduler(context, update):
    print(update.effective_chat.id, ":", "launched income scheduler")
    # do it every hour
    schedule.every(60).minutes.do(auto_update_info, context=context, update=update)
    
    while(True):
        schedule.run_pending()

# TODO: need to rename
def auto_update_info(context, update):
    print(update.effective_chat.id, ":", "auto update income info")
    goal_income = 300
    data = get_data()

    if (goal_income <= float(data['income'])):
        arg_str = "Congratulations! Goal achieved! Your income:" + str(data['income']) + "Rub"
        send_message(context, update.effective_chat.id, arg_str)

def send_message(context, chat_id, str):
    context.bot.sendMessage(chat_id, str)

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
    updater = Updater(token = 'put your token here', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handler_start))
    dispatcher.add_handler(CommandHandler("get_cost", handler_get_cost))
    dispatcher.add_handler(CommandHandler("get_income", handler_get_income))
    dispatcher.add_handler(CommandHandler("get_auto_info", handler_get_auto_info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()