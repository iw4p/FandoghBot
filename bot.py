#Importing Modules
try:
    import sys
    import time
    import requests
    import json
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, CallbackQueryHandler
    import logging
except ImportError as e:
	print("Problem: ",e)
	exit()


BASE_URL = "https://api.fandogh.cloud/api/"


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class Login:
    email = ''
    namespaces = []
    username = ''
    token = ''
    is_staff = bool

loginInfo = Login()

def start(update, context):

        hour = int(time.strftime("%H"))

        text = ''
 
        if hour >= 0 and hour <= 11:
                text="Good Morning!"

        elif hour >= 12 and hour <= 18:
                text="Good Afternoon!"

        elif hour >= 17 and hour <= 23:
                text="Good Evening!"

        update.message.reply_text(text + "\n\nFor Sign In please use command like this\n/login Username Password")


def login(update, context):
    """Command handler: /login <username> <password>"""
    # logging.info(f"Command: /login triggered by {update.effective_chat.id}")
    if len(context.args) != 2:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Not enough or too many parameters, I need both usernamae and password.",
        )
    else:        
        response = getLoginInfo(context.args[0],context.args[1])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
        )



def help_command(update, context):
    update.message.reply_text("Use /login Username Password to login again.")

def getLoginInfo(username, password):
    global BASE_URL
    response = requests.post(BASE_URL + "tokens", data = {'username':username,'password':password})
    if response.status_code == 200:
        json_response = response.json()
        loginInfo.email = json_response['email']
        loginInfo.namespaces = json_response['namespaces']
        loginInfo.username = json_response['username']
        loginInfo.token = json_response['token']
        loginInfo.is_staff = json_response['is_staff']
        return loginInfo.token
    else:
        return response.json()['message']


def main():

    # First arg as bot token
    tokenParam = sys.argv[1] 

    # Create the Updater and pass it your bot's token.
    updater = Updater(tokenParam, use_context=True)

    dp = updater.dispatcher


    dp.add_handler(CommandHandler('start', start))

    login_handler = CommandHandler('login', login, pass_args=True)
    dp.add_handler(login_handler)


    dp.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()