# @Author: Daniil Maslov (ComicSphinx)

import requests, json, logging, time, schedule
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from multiprocessing.pool import ThreadPool

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level = logging.INFO)

logger = logging.getLogger(__name__)

flag_goal_achieved = False

def handler_start(update, context):
    print(update.effective_chat.id, ":", "was connected and used /start")

    update.message.reply_text("Hello!")
    update.message.reply_text("Use /get_cost to get cost")
    update.message.reply_text("Use /get_income to get income")
    update.message.reply_text("Use /set_goal <value> to set goal")

def get_data():
    data = requests.get("http://127.0.0.1:5000/get/id")
    data = data.json()
    return data

def handler_get_cost(update, context):
    print(update.effective_chat.id, ":", "/get_cost")
    data = get_data()
    update.message.reply_text("Investment portfolio value: " + str(data['cost']) + "Rub")

def handler_get_income(update, context):
    print(update.effective_chat.id, ":", "/get_income")
    data = get_data()
    update.message.reply_text("Investment portfolio income: " + str(data['income']) + "Rub")

#TODO: В этой функции буду получать goal_value прямо из чата.
def handler_set_goal(update, context):
    print(update.effective_chat.id, ":", "/set_goal")
    goal_value = 300
    #TODO: Нужно ли убивать этот поток после выполнения?
    pool = ThreadPool(processes=1)
    get_parse_data = pool.apply_async(scheduler_income_goal, args=(context, update, goal_value))

def scheduler_income_goal(context, update, goal_value):
    print(update.effective_chat.id, ":", "launched income scheduler")

    schedule.every(5).seconds.do(track_goal, context=context, update=update, goal_value=goal_value)

    while(flag_goal_achieved == False):
        schedule.run_pending()

def track_goal(context, update, goal_value):
    print(update.effective_chat.id, ":", "launched tracking goal")
    data = get_data()

    if (goal_value <= float(data['income'])):
        print(update.effective_chat.id, ":", "Goal achieved")
        global flag_goal_achieved
        flag_goal_achieved = True

        arg_str = "Congratulations! Goal achieved! Your income:" + str(data['income']) + "Rub"
        context.bot.sendMessage(update.effective_chat.id, arg_str)

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
    dispatcher.add_handler(CommandHandler("set_goal", handler_set_goal))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()