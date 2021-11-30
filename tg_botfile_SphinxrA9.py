import shelve
import logging
import random
from uuid import uuid4
import translators as ts

from telegram import Update, ForceReply, InlineQueryResultArticle,InlineQueryResultPhoto, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
from telegram.utils.helpers import escape_markdown

class Riddle:
    """global list for riddle"""
    def __init__(self ): # ,head = None , body = None ,answer = None
        self.l_riddle = []




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

def gj_get_answer(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Да ! , это / %s / \n Молодец :) \n ну или ты просто угадал одно слово в ответе,тогда молодец, но не такой большой \n в общем поздравляю, мишка тобой доволен ʕ ᵔᴥᵔ ʔ ' %
        ridddle_user.l_riddle[2])
    ridddle_user.l_riddle = []



def try_get_hint(update: Update, context: CallbackContext, inline_mode = 'off') -> None:
    if len(ridddle_user.l_riddle) == 4:
        hint = 'Hint: %s ' % ridddle_user.l_riddle[3]
        if inline_mode == 'on':
            return hint
        update.message.reply_text(hint)
    else:
        fail_hint = 'у этой загадки не было подсказки , сорян ¯\_(ツ)_/¯ '
        if inline_mode == 'on':
            return fail_hint
        update.message.reply_text(fail_hint)

def skip_riddle(update: Update, context: CallbackContext , inline_mode = 'off') -> None:
    message = ('сдаёшься?Ну ладно .... \n Вот ответ : \n %s ' % ridddle_user.l_riddle[2])
    if inline_mode == 'off':
        update.message.reply_text(message)
    ridddle_user.l_riddle = []
    return message

def riddlle_in_list(update: Update, context: CallbackContext) -> None:
    if update.message.text.lower() in ridddle_user.l_riddle[2].replace('"','').lower().split():
        gj_get_answer(update,context)
    elif 'help' in update.message.text.lower() or 'подсказка' in update.message.text.lower() or 'hint' in update.message.text.lower():
        try_get_hint(update,context)
    elif 'skip' in update.message.text.lower() or 'сда' in update.message.text.lower():
        skip_riddle(update,context)
    else:
        update.message.reply_text('неа, не угадал)')


def get_riddle(update: Update, context: CallbackContext, inline_mode = 'off') -> None:
    #работает, но чёт выглядит как говно , подумать .. потом)
    if inline_mode == 'on': # update.message.text в инлайн режиме нельзя создать, приходиться костыльно перименовывать
        upd_message = 'random'
    elif inline_mode == 'off':
        upd_message = update.message.text

    if 'random' in upd_message.lower() or 'случай' in upd_message.lower():
        random_number = random.randint(0, len(shelve.open('riddle_tuples.db')))
        # update.message.text = random.randint(0, len(shelve.open('riddle_tuples.db'))+1)
        upd_message = random_number

    user_text = int(upd_message)
    list_riddle_len = len(shelve.open('riddle_tuples.db'))
    if user_text in range(list_riddle_len):  # а как хранить к подсказку?м?
        for value in (shelve.open('riddle_tuples.db')[str(user_text)]):
            ridddle_user.l_riddle.append(value)
        message = 'Название : %s \n текст: %s' % (ridddle_user.l_riddle[0], ridddle_user.l_riddle[1])
        if inline_mode == 'on': #выход из функции(для инлайн режима)
            return message
        update.message.reply_text(message)
    else:
        update.message.reply_text('С таким номером не существует , диапазон № %2d ' % list_riddle_len)

def cant_get_hint(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Вы ещё ничего не загадали :/')

def dont_get_riddle(update: Update, context: CallbackContext) -> None:
    try:
        get_riddle(update,context)
    except:
        if 'help' in update.message.text.lower() or 'подсказ' in update.message.text.lower() or 'hint' in update.message.text.lower():
            cant_get_hint(update,context)
        else:
            update.message.reply_text('Вы неккорректно указали комманду  :) ')


def riddle_in_range(update: Update, context: CallbackContext) -> None:
    # можно попробовать без ключевого слова а через if answer in text
    # 1 проблема == кавычки и пр залупа
    # 2я эту котлетку нужно раскидать по функциям, или она эволиционирует к стрёмного гомункула(уже?)
    # 3 == инлайн режим
    # при вводе 2й буквы ремувит на пустой лист, потов возвращет назад список на место(при 3й букве) и так по кругу...
    #проблема в том что я не могу нормально переиспользовать этот код для инлайна т.к разные классы/комманды.
    # ... даже если нормально заспличу по функциям , при этом он не скипает загадку и продлолжает предлагать его пока ты не жмякнешь куда либ
    # о (например на хинт)
    if len(ridddle_user.l_riddle) != 0 :
        riddlle_in_list(update,context)

    else:
        dont_get_riddle(update,context)
#создаётся, не детектит 1ю букву и чистится..

def riddle_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Диапазон возможных номеров от 0 до %2d '%len(shelve.open('riddle_tuples.db')))



def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    test_img = 'https://icdn.lenta.ru/images/2021/04/27/16/20210427163138131/detail_9b31eaf4376cdff03e0ba1bcaa826a01.jpg'
    if query == "":
        return

    if len(ridddle_user.l_riddle) == 0:
        print(ridddle_user.l_riddle)
        random_or_hint = InlineQueryResultArticle(
            id=str(uuid4()),
            title="Random_R",
            input_message_content=InputTextMessageContent(get_riddle(update, context, 'on')),
        )
        skip_or_cat = InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url = test_img,
            thumb_url = test_img,
            title="Cats",
        )
        check_answer_or_ASCII = InlineQueryResultArticle(
            id=str(uuid4()),
            title="ASCII",
            input_message_content=InputTextMessageContent(
                '. ,_,\n(O,O)\n (   )\n-"-"-- '
            ),
        )
    elif len(ridddle_user.l_riddle) != 0:
        print(ridddle_user.l_riddle)
        random_or_hint = InlineQueryResultArticle(
            id=str(uuid4()),
            title="hint",
            input_message_content=InputTextMessageContent(try_get_hint(update,context,'on')), # ВАЖНОЕ ПРИМЕЧАНИЕ ДЛЯ ХИНТА НУЖЕНН ДРУГОЙ ТЕКСТ В НАБОРЕ(Т.К ОН НЕ АПДЕЙТИТ ЛУЛ)
        )

        # if query.strip().lower() in ridddle_user.l_riddle[2].replace('"', '').lower().split():
        #     check_answer = 'Да ! , это / %s / \n Молодец :) \n ну или ты просто угадал одно слово в ответе,тогда молодец, но не такой большой \n в общем поздравляю, мишка тобой доволен ʕ ᵔᴥᵔ ʔ ' %ridddle_user.l_riddle[2]
        #     ridddle_user.l_riddle = []
        #     #поидее проблема если где и может быть то здесь , но она не уходит при комменте(
        # else:
        #     check_answer = 'не,не угадала'
        check_answer_or_ASCII = InlineQueryResultArticle(
            id=str(uuid4()),
            title="check answer",
            input_message_content=InputTextMessageContent('check_answer'),
        )
        skip_or_cat = InlineQueryResultArticle(
            id=str(uuid4()),
            title="skip",
            input_message_content=InputTextMessageContent(skip_riddle(update, context, 'on')),
            # ВАЖНОЕ ПРИМЕЧАНИЕ ДЛЯ ХИНТА НУЖЕНН ДРУГОЙ ТЕКСТ В НАБОРЕ(Т.К ОН НЕ АПДЕЙТИТ ЛУЛ)
        )

    results = [
        random_or_hint,
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="translate on en",
            input_message_content=InputTextMessageContent(ts.google(query)),
        ),
       InlineQueryResultArticle(
           id=str(uuid4()),
           title="translate on ru",
           input_message_content=InputTextMessageContent(ts.google(query,from_language='auto', to_language='ru')),
       ),
        skip_or_cat,
        check_answer_or_ASCII,
    ]

    update.inline_query.answer(results)

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

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    #пользователей заносить в бд как?
    ridddle_user = Riddle()
    main()

