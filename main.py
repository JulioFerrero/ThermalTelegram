import logging

from PIL import Image
from decouple import config
from escpos.printer import *
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

p = Usb(0x28e9, 0x0289)
p.set(align='center')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
    )


def echo(update: Update, _: CallbackContext) -> None:
    """Print text."""
    p.text(update.effective_user.first_name)
    p.text(update.message.date.strftime("%m/%d/%Y, %H:%M:%S"))
    p.text('\n')
    p.text('~~~')
    p.text('\n')
    p.text(update.message.text)
    p.text('\n')
    p.text('\n')


def images(update: Update, _: CallbackContext) -> None:
    """Print image."""
    newImageName = update.message.photo[-1].file_id + '.png'
    update.message.photo[-1].get_file().download('./rawImages/' + newImageName)
    image = Image.open('./rawImages/' + newImageName)
    image.thumbnail((375, 9000))
    image.save('./outImages/' + newImageName)
    p.image('./outImages/' + newImageName)
    p.text('\n')
    p.text('\n')


def stickers(update: Update, _: CallbackContext) -> None:
    """Print sticker."""
    newStickerName = update.message.sticker.file_id + '.png'
    update.message.sticker.get_file().download('./rawStickers/' + newStickerName)
    sticker = Image.open('./rawStickers/' + newStickerName)
    sticker.thumbnail((375, 9000))
    sticker.save('./outStickers/' + newStickerName)
    p.image('./outStickers/' + newStickerName)
    p.text('\n')
    p.text('\n')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(config('TOKEN'))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo, images))
    dispatcher.add_handler(MessageHandler(Filters.sticker, stickers))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
