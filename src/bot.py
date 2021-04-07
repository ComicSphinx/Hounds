# @Author: Daniil Maslov (ComicSphinx)

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
from multiprocessing.pool import ThreadPool
import hound_parser

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level = logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Hello!")
    update.message.reply_text("Use /get_cost to get cost")
    update.message.reply_text("Use /get_income to get income")

def get_cost(update: Update, _: CallbackContext) -> None:
    pool = ThreadPool(processes=1)
    cost = pool.apply_async(hound_parser.parse_cost)
    cost = cost.get()
    update.message.reply_text("Стоимость портфеля: " + cost)

def get_income(update: Update, _: CallbackContext) -> None:
    pool = ThreadPool(processes=1)
    income = pool.apply_async(hound_parser.parse_income)
    income = income.get()
    update.message.reply_text("Прибыль: " + income)

def main():
    updater = Updater(token = 'put your token here', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("get_cost", get_cost))
    dispatcher.add_handler(CommandHandler("get_income", get_income))
    
    updater.start_polling()
    updater.idle()
    

if __name__ == '__main__':
    main()
