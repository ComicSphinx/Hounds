# @Author: Daniil Maslov (ComicSphinx)

import requests, json, logging, time, schedule
from telegram.ext import Updater, CommandHandler, CallbackContext
from multiprocessing.pool import ThreadPool
import databaseUtilities as dbu

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level = logging.INFO)

logger = logging.getLogger(__name__)

flag_goal_achieved = False

def handler_start(update, context):
    print(update.effective_chat.id, ":", "used /start or /help")

    dbu.addUser(update.effective_chat.id)

    update.message.reply_text("Use /help to get help with commands")
    update.message.reply_text("Use /get_cost to get cost")
    update.message.reply_text("Use /get_income to get income")
    update.message.reply_text("Use /set_goal <value> to set goal")
    update.message.reply_text("Use /set_page_url <url> to set portfolio url")

def get_data(chat_uid):
    user_data = dbu.get_user(chat_uid)
    url = user_data[0][1]
    data = requests.get("http://127.0.0.1:5000/get/"+str(url))
    data = data.json()
    return data

def handler_get_cost(update, context):
    print(update.effective_chat.id, ":", "/get_cost")
    data = get_data(update.effective_chat.id)
    update.message.reply_text("Investment portfolio value: " + str(data['cost']) + "Rub")

def handler_get_income(update, context):
    print(update.effective_chat.id, ":", "/get_income")
    data = get_data(update.effective_chat.id)
    update.message.reply_text("Investment portfolio income: " + str(data['income']) + "Rub")

def handler_set_goal(update, context):
    print(update.effective_chat.id, ":", "/set_goal")
    global flag_goal_achieved
    flag_goal_achieved = False

    try:
        goal_value = int(context.args[0])
        print(update.effective_chat.id, ": set goal -", goal_value)
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /set_goal <value>")
    
    #TODO: Нужно ли убивать этот поток после выполнения?
    pool = ThreadPool(processes=1)
    get_parse_data = pool.apply_async(scheduler_income_goal, args=(context, update, goal_value))
    update.message.reply_text("Goal successfully setted.")

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

def handler_set_page_url(update, context):
    print(update.effective_chat.id, ":", "/set_page_url")

    try:
        portfolio_url = str(context.args[0])
        column = "portfolio_url"
        print(update.effective_chat.id, "trying to add portfolio url = ", portfolio_url)
        dbu.addData(update.effective_chat.id, column, portfolio_url)

    except (IndexError, ValueError):
        print(update.effective_chat.id, ": failed attempt to set portfolio url")
        update.message.reply_text("Usage: /set_page_url <url>")

def main():
    if (dbu.verifyDatabaseExist() == 0):
        print("Database is not exists")
        dbu.createDB()
        print("Database created")
    elif (dbu.verifyDatabaseExist() == 1):
        print("Database found")

    updater = Updater(token = 'put your token here', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handler_start))
    dispatcher.add_handler(CommandHandler("help", handler_start))
    dispatcher.add_handler(CommandHandler("get_cost", handler_get_cost))
    dispatcher.add_handler(CommandHandler("get_income", handler_get_income))
    dispatcher.add_handler(CommandHandler("set_goal", handler_set_goal))
    dispatcher.add_handler(CommandHandler("set_page_url", handler_set_page_url))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()