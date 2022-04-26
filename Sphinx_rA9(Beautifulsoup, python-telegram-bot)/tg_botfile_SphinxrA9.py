import shelve
import logging
import random
from uuid import uuid4
import translators as ts
from token_key import TOKEN

from telegram import Update, ForceReply, InlineQueryResultArticle,InlineQueryResultPhoto, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
from telegram.utils.helpers import escape_markdown

class Riddle:
    """global list for riddle"""
    def __init__(self ):
        self.l_riddle = []


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Вы можете играть со мной как с обычнам ботом ( диапазон возможных номеров от 0 до %2d ).. или просто напешите random :) \n или испольовать меня в inline режиме , просто тэгните меня через собаку @ \n Комманды : get_riddle , skip_riddle '%len(shelve.open('riddle_tuples.db')))

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
    if inline_mode == 'on': # update.message.text в инлайн режиме нельзя создать, приходиться костыльно перименовывать
        upd_message = 'random'
    elif inline_mode == 'off':
        upd_message = update.message.text
    list_riddle_len = int(len(shelve.open('riddle_tuples.db')))
    if 'random' in upd_message.lower() or 'случай' in upd_message.lower() :
        upd_message = random.randint(0, list_riddle_len)

    user_text = int(upd_message)
    # list_riddle_len = len(shelve.open('riddle_tuples.db'))
    if user_text in range(list_riddle_len):
        for value in (shelve.open('riddle_tuples.db')[str(user_text)]):
            ridddle_user.l_riddle.append(value)
        message = 'Название : %s \n текст: %s' % (ridddle_user.l_riddle[0], ridddle_user.l_riddle[1])
        if inline_mode == 'on': #выход из функции(для инлайн режима)
            return str(message)
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
    if len(ridddle_user.l_riddle) != 0 :
        riddlle_in_list(update,context)
    else:
        dont_get_riddle(update,context)


def riddle_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Диапазон возможных номеров от 0 до %2d '%len(shelve.open('riddle_tuples.db')))

def button_get_riddle(update: Update, context: CallbackContext) -> None:
    gets_riddle = InlineQueryResultArticle(
            id=str(uuid4()),
            title="Random_R",
            input_message_content=InputTextMessageContent(get_riddle(update, context,'on')),
        )
    #возможно нужна запятая
    return gets_riddle

def none_in_list_inline(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if len(ridddle_user.l_riddle) == 0:
        buttons = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="нету активной загадки",
                input_message_content=InputTextMessageContent(
                    'что бы взять нужно @ тэгнуть этого бота +ввести комманду  "get_riddle" + пробел )'
                ),),]
    if 'get_riddle' in query:
        buttons = [(button_get_riddle(update,context))]
    return buttons

def button_check_answer(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if query.strip().lower() in ridddle_user.l_riddle[2].replace('"', '').lower().split():
        check_answer = 'можешь жать скип, если думаешь, что отгадала'
    else:
        check_answer = 'не,не такого слова в ответе нет'
    button_check =  InlineQueryResultArticle(
            id=str(uuid4()),
            title="check answer",
            input_message_content=InputTextMessageContent(check_answer),)
            #пока не работающая функция ( нужно закрыть бажик сначала)
    return button_check

def button_skip_riddle(update: Update, context: CallbackContext) -> None:
    button_skip = InlineQueryResultArticle(
            id=str(uuid4()),
            title="skip",
            input_message_content=InputTextMessageContent(skip_riddle(update, context, 'on')),)
    return button_skip

def riddle_in_list_inline(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    buttons =  [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="hint",
            input_message_content=InputTextMessageContent(try_get_hint(update, context, 'on')),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="прочитать загадку",
            input_message_content=InputTextMessageContent('Название : %s \n текст: %s' % (ridddle_user.l_riddle[0], ridddle_user.l_riddle[1])),
        ),
    ]
    if query in ridddle_user.l_riddle[2]: #поработать с функцией
        buttons.append(button_check_answer(update, context))

    if 'skip_riddle' in query:
        buttons.append(button_skip_riddle(update,context))
    if 'get_riddle' in query:
        ridddle_user.l_riddle = []
        buttons.append(get_riddle(update, context, 'on'))
    return buttons

def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if query == "":
        return
    if len(ridddle_user.l_riddle) == 0:
        buttons = none_in_list_inline(update,context)
    elif len(ridddle_user.l_riddle) != 0:
        buttons = riddle_in_list_inline(update, context)

    all_buttons = [
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
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="ASCII",
            input_message_content=InputTextMessageContent(
                '. ,_,\n(O,O)\n (   )\n-"-"-- '
            ),
        )]
    for button in buttons:
        print(str(button))
        all_buttons.append(button)

    update.inline_query.answer(all_buttons)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN) # insert your token here (replace TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("Riddle", riddle_command))


    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, riddle_in_range))


    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    #пользователей заносить в бд 
    print('check restart')
    ridddle_user = Riddle()
    main()
