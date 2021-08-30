from apiFootBall import apiFootBall as res
import logging
from typing import Tuple, Dict, Any
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
    callbackcontext,
)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# State definitions for top level conversation
SELECTING_LEAGUE, TABLE_LIST, SHOWRES = map(
    chr, range(3))

# Definitions for 5 Big Leagues
PREMIER_L, SPANISH_L, ITALY_L, GERMANY_L, FRENCH_L = map(chr, range(3, 8))

# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(
    STANDING,
    TOP_SCORER,
    TOP_ASSISTS,
    BACK,
    START_OVER,

) = map(chr, range(8, 13))


# Start Method
def start(update: Update, context: CallbackContext) -> str:
    """Select an action: Adding parent/child or show data."""
    text = (
        "You may choose one of the big leagues , or end the "
        "conversation. To abort, simply type /stop."
    )

    buttons = [
        [
            InlineKeyboardButton(text='Premier League',
                                 callback_data=str(PREMIER_L)),
        ],
        [
            InlineKeyboardButton(text='La Liga', callback_data=str(SPANISH_L)),
        ],
        [
            InlineKeyboardButton(text='Serie A', callback_data=str(ITALY_L)),
        ],
        [
            InlineKeyboardButton(
                text='Bundesliga', callback_data=str(GERMANY_L)),
        ],
        [
            InlineKeyboardButton(text='Ligue 1', callback_data=str(FRENCH_L)),
        ],

        [
            InlineKeyboardButton(text='Done', callback_data=str(END)),
        ],

    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(
            "Hi, I'm iFootBall Bot.\n"
            "POWERED PY: @iNecoTiNe"
        )
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = True
    return SELECTING_LEAGUE


def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    context.user_data[START_OVER] = False
    update.message.reply_text("Okay, bye.")
    return END


def end(update: Update, context: CallbackContext) -> int:
    """End conversation from InlineKeyboardButton."""
    context.user_data[START_OVER] = False
    update.callback_query.answer()
    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)
    return END


def selectPL(update: Update, context: CallbackContext):
    context.user_data['choice'] = PREMIER_L
    return selectTable(update, context)


def selectSL(update: Update, context: CallbackContext):
    context.user_data['choice'] = SPANISH_L
    return selectTable(update, context)


def selectIL(update: Update, context: CallbackContext):
    context.user_data['choice'] = ITALY_L
    return selectTable(update, context)


def selectGL(update: Update, context: CallbackContext):
    context.user_data['choice'] = GERMANY_L
    return selectTable(update, context)


def selectFL(update: Update, context: CallbackContext):
    context.user_data['choice'] = FRENCH_L
    return selectTable(update, context)


# back01
def BackSelectLeague(update: Update, context: CallbackContext):
    context.user_data['choice'] = None
    start(update, context)
    return SELECTING_LEAGUE


# back02
def BackTableList(update: Update, context: CallbackContext):
    update.callback_query.answer()
    return selectTable(update, context)


def selectTable(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton(text='Table',
                                 callback_data=str(STANDING)),
            InlineKeyboardButton(text='Top Scorers',
                                 callback_data=str(TOP_SCORER)),
        ],
        [
            InlineKeyboardButton(text='Top Assists',
                                 callback_data=str(TOP_ASSISTS)),
            InlineKeyboardButton(text='Back',
                                 callback_data=str(END)),
        ],

    ]
    keyboard = InlineKeyboardMarkup(buttons)
    name = getName(context.user_data['choice'])
    update.callback_query.edit_message_text(
        text=f'You chouse : {name} , Ok select one of the tables to show information', reply_markup=keyboard)
    return TABLE_LIST


# Standing Function
def standing(update: Update, context: CallbackContext):
    id = getId(context.user_data['choice'])
    obj = res(update)
    text = obj.standingPyId(id)
    del obj
    return showRes(update, context, text)


def scorers(update: Update, context: CallbackContext):
    id = getId(context.user_data['choice'])
    obj = res(update)
    text = obj.scorersPyId(id)
    del obj
    return showRes(update, context, text)


def assists(update: Update, context: CallbackContext):
    id = getId(context.user_data['choice'])
    obj = res(update)
    text = obj.assistsPyId(id)
    del obj
    return showRes(update, context, text)


def showRes(update: Update, context: CallbackContext, text: str):
    update.callback_query.answer()
    buttons = [
        [
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard, parse_mode='MarkdownV2')

    return SHOWRES


# helper Methods
def getId(choice) -> str:
    if choice == PREMIER_L:
        return "39"
    elif choice == SPANISH_L:
        return "140"
    elif choice == ITALY_L:
        return "135"
    elif choice == GERMANY_L:
        return "78"
    elif choice == FRENCH_L:
        return "61"
    else:
        return None


def getName(choice) -> str:
    if choice == PREMIER_L:
        return "Premier League"
    elif choice == SPANISH_L:
        return "La Liga"
    elif choice == ITALY_L:
        return "Serie A"
    elif choice == GERMANY_L:
        return "Bundesliga"
    elif choice == FRENCH_L:
        return "Ligue 1"
    else:
        return None


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1987491068:AAFzbN7xYyal3_XfSjGNgcUomwcoX_zoo2M")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_LEAGUE: [
                CallbackQueryHandler(
                    selectPL, pattern='^' + str(PREMIER_L) + '$'),
                CallbackQueryHandler(
                    selectSL, pattern='^' + str(SPANISH_L) + '$'),
                CallbackQueryHandler(
                    selectIL, pattern='^' + str(ITALY_L) + '$'),
                CallbackQueryHandler(
                    selectGL, pattern='^' + str(GERMANY_L) + '$'),
                CallbackQueryHandler(
                    selectFL, pattern='^' + str(FRENCH_L) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
            ],
            TABLE_LIST: [
                CallbackQueryHandler(standing, pattern='^' +
                                     str(STANDING) + '$'),
                CallbackQueryHandler(scorers, pattern='^' +
                                     str(TOP_SCORER) + '$'),
                CallbackQueryHandler(assists, pattern='^' +
                                     str(TOP_ASSISTS) + '$'),
                CallbackQueryHandler(
                    BackSelectLeague, pattern='^' + str(END) + '$'),

            ],
            SHOWRES: [CallbackQueryHandler(
                BackTableList, pattern='^' + str(END) + '$'), ]

        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
