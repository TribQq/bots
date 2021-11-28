import shelve
import logging
import random

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


class Riddle:
    def __init__(self ): # ,head = None , body = None ,answer = None
        self.l_riddle = []
        # self.head = head
        # self.body = body
        # self.answer = answer



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!_command ' )


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def riddle_in_range(update: Update, context: CallbackContext) -> None:
    #нужно передать в эту переменную текст(а он уже лежит в классе лул)
    # можно попробовать без ключевого слова а через if answer in text
    #блэт , ну а так даже 1 рандомная буква может разлочить.. ( можно засплитать текст на слова?)
    # 1 проблема == кавычки и пр залупа
    # 2я эту котлетку нужно раскидать по функциям, или она эволиционирует к стрёмного гомункула(уже?)
    # 3 == инлайн режим
    if len(ridddle_user.l_riddle) != 0 :
        if update.message.text == ridddle_user.l_riddle[2] or update.message.text in ridddle_user.l_riddle[2].replace('"','').split():
            update.message.reply_text('Да ! , это / %s / \n Молодец :) \n ну или ты просто угадал одно слово в ответе,тогда молодец, но не такой большой \n в общем поздравляю, мишка тобой доволен ʕ ᵔᴥᵔ ʔ ' %ridddle_user.l_riddle [2])
            ridddle_user.l_riddle = []
        elif 'help' in update.message.text.lower() or 'подсказка' in update.message.text.lower() or 'hint' in update.message.text.lower():
            if len(ridddle_user.l_riddle) == 4:
                update.message.reply_text('Hint: %s '%ridddle_user.l_riddle[3])
            else:
                update.message.reply_text('у это загадки не было подсказки , сорян ¯\_(ツ)_/¯ ')
        elif 'skip' in update.message.text.lower() or 'сда' in update.message.text.lower():
            update.message.reply_text('сдаёшься?Ну ладно .... \n Вот ответ : \n %s ' %ridddle_user.l_riddle [2] )
            ridddle_user.l_riddle = []
        else:
            update.message.reply_text('неа, не угадал)')

    else:
        try:
            if 'random' in update.message.text.lower() or 'случай' in update.message.text.lower():
                random_number = random.randint(0, len(shelve.open('riddle_tuples.db')))
                # update.message.text = random.randint(0, len(shelve.open('riddle_tuples.db'))+1)
                update.message.text = random_number

            user_text = int(update.message.text)
            list_riddle_len = len(shelve.open('riddle_tuples.db'))
            if user_text in range(list_riddle_len):#а как хранить к подсказку?м?
                for value in (shelve.open('riddle_tuples.db')[str(user_text)]):
                    ridddle_user.l_riddle.append(value)

                update.message.reply_text('Название : %s \n текст: %s'%(ridddle_user.l_riddle[0] , ridddle_user.l_riddle[1]))
            else:
                update.message.reply_text('С таким номером не существует , диапазон № %2d ' %list_riddle_len)
        except:
            if 'help' in update.message.text.lower() or 'подсказ' in update.message.text.lower() or 'hint' in update.message.text.lower():
                update.message.reply_text('Вы ещё ничего не загадали :/')
            else:
                update.message.reply_text('Вы неккорректно указали комманду  :) ')



def riddle_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Диапазон возможных номеров от 0 до %2d '%len(shelve.open('riddle_tuples.db')))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2100416145:AAE2JL23QIQ5L7ep0-zlhkqrjzlDds0E7jw")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("Riddle", riddle_command))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, riddle_in_range))

    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    ridddle_user = Riddle()
    main()

