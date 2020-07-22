#Start
#Importing Modules
try:
    import sys
    import time
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, CallbackQueryHandler
    import logging
except ImportError as e:
	print("Problem: ",e)
	exit()

login_post = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class LoginInfo:
        email = ''
        password = ''


credentials = LoginInfo()




def start(update, context):

        hour = int(time.strftime("%H"))

        text = ''

        credentials.email = ''
        credentials.password = ''

        if hour >= 0 and hour <= 11:
                text="Good Morning!"

        elif hour >= 12 and hour <= 18:
                text="Good Afternoon!"

        elif hour >= 17 and hour <= 23:
                text="Good Evening!"

        keyboard = [[InlineKeyboardButton("Login", callback_data='1')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(text)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)




# def login(bot, update, args):
#     if len(args) > 1:
#         username = args[0]
#         password = args[1]
#         global login_post
#         login_post = {
#             'username': username.lower(),
#             'password': password
#         }
#         bot.sendMessage(chat_id=update.message.chat_id, text="Now you can send private url of photo or video of your private friends.")
#         print(username, password)
#     else:
#         bot.sendMessage(chat_id=update.message.chat_id, text="Try again. Use /login username password.")

def login(update, context):
    """Command handler: /login <username> <password> - save login to database."""
    logging.info(f"Command: /login triggered by {update.effective_chat.id}")
    if len(context.args) != 2:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Not enough or too many parameters, I need both usernamae and password.",
        )
    else:
        print(context.args)

                        


# def loginButton(update, context):
#     query = update.callback_query

#     query.answer()

#     query.edit_message_text(text="Enter your username: ")

def getUserText(update, context):
    text = update.message.text
    print(text)
    return text

def help_command(update, context):
    update.message.reply_text("Use /start to login again.")

def getToken():
    # api.fandogh.cloud/api/tokens
    print("get token")


def main():

    # First arg as bot token
    tokenParam = sys.argv[1] 

    # Create the Updater and pass it your bot's token.
    updater = Updater(tokenParam, use_context=True)

    dp = updater.dispatcher


    dp.add_handler(CommandHandler('start', start))
    # dp.add_handler(CallbackQueryHandler(loginButton))
    # dp.add_handler(MessageHandler(Filters.text, getUserText))

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