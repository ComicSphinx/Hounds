# @Author: Daniil Maslov (ComicSphinx)

from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext
from multiprocessing.pool import ThreadPool
import logging, time, hound_parser

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level = logging.INFO)

logger = logging.getLogger(__name__)

def handler_start(update, context):
    update.message.reply_text("Hello!")
    update.message.reply_text("Use /get_cost to get cost")
    update.message.reply_text("Use /get_income to get income")
    update.message.reply_text("Use /get_auto_info")

def handler_get_cost(update: Update, _: CallbackContext) -> None:
    pool = ThreadPool(processes=1)
    cost = pool.apply_async(hound_parser.parse_cost)
    cost = cost.get()
    update.message.reply_text("Стоимость портфеля: " + cost)

def handler_get_income(update: Update, _: CallbackContext) -> None:
    pool = ThreadPool(processes=1)
    income = pool.apply_async(hound_parser.parse_income)
    income = income.get()
    update.message.reply_text("Прибыль: " + income)

def handler_get_auto_info(update: Update, _: CallbackContext) -> None:
    print("/get_auto_info")
    # goal income in RUB
    goal_income = 290
    # wait 60 minutes
    time_wait = 60 * 60
    while(True):
        time.sleep(time_wait)
    
        # get income
        pool = ThreadPool(processes=1)
        get_parse_data = pool.apply_async(hound_parser.parse_income)
        current_income = get_parse_data.get()

        if (goal_income <= float(current_income)):
            update.message.reply_text("Цель достигнута! Ваш доход:" + current_income)

def main():
    updater = Updater(token = 'yourToken', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handler_start))
    dispatcher.add_handler(CommandHandler("get_cost", handler_get_cost))
    dispatcher.add_handler(CommandHandler("get_income", handler_get_income))
    dispatcher.add_handler(CommandHandler("get_auto_info", handler_get_auto_info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
