from telegram import Update, Bot
from telegram.ext import CallbackContext, CommandHandler
from functools import wraps
import config

def owner_only(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user = update.effective_user
        if user and user.id == config.OWNER_ID:
            return func(update, context, *args, **kwargs)
        else:
            update.message.reply_text("You don't have permission to use this command.")
            return context.bot.stop_job(update.message.chat_id)
    return wrapper

# Example usage:
@owner_only
def my_command(update: Update, context: CallbackContext):
    # Only the owner can execute this command
    pass

def main():
    bot = Bot(config.TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('my_command', my_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
