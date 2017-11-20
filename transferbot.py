#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This bot downloads attachments then uploads them to transfer.sh
"""

from telegram.ext   import Updater, CommandHandler, MessageHandler
from telegram.ext   import Filters, CallbackQueryHandler
import logging
import re
import requests

#   LOGGER
logging.basicConfig (format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger (__name__)

def transfer (filename):
    """Sends filename then deletes it. Returns url"""
    upload_url = "https://transfer.sh/" + filename
    #r = requests.put(url=upload_url, files={filename: open(filename, "r+")})
    r = requests.put(url=upload_url, data=open(filename, "r"))
    return (r.text.strip())

#   HANDLERS
def cmd_start (bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text ('Transferbot 0.1')

def cmd_help (bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text ('TODO /help')

def cmd_halt (bot, update):
    """ TODO """

def cmd_unknown (bot, update):
    """Send a message if the command is not defined."""
    update.message.reply_text ('Command not found. Type /help for... help.')

def cmd_error (bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning ('Update "%s" caused error "%s"', update, error)

#   ATTACHMENT's FALLBACKS
def fbk_document (bot, update):
    """Get document, then transfer() it"""
    update.message.reply_text ('Got ' + update.message.document.file_name)
    update.message.reply_text ('MIME ' + update.message.document.mime_type)
    user        = update.message.from_user
    document    =  bot.get_file(update.message.document.file_id)
    document.download (update.message.document.file_name)
    logger.info ("Got document from %s: %s", user.first_name, update.message.document.file_name)
    update.message.reply_text (transfer (update.message.document.file_name))

def fbk_audio (bot, update):
    """Get audio, then transfer() it"""
    update.message.reply_text ('Got ' + update.message.audio.file_id)
    update.message.reply_text ('MIME ' + update.message.audio.mime_type)
    ext         = re.findall(r'/(\w+)', update.message.audio.mime_type)[0]
    filename    = update.message.audio.file_id + '.' + ext
    user        = update.message.from_user
    document    =  bot.get_file(update.message.audio.file_id)
    document.download (filename)
    logger.info ("Got audio from %s: %s", user.first_name, filename)
    update.message.reply_text (transfer (filename))

def fbk_video (bot, update):
    """Get video, then transfer() it"""
    update.message.reply_text ('Got ' + update.message.video.file_id)
    update.message.reply_text ('MIME ' + update.message.video.mime_type)
    ext         = re.findall(r'/(\w+)', update.message.video.mime_type)[0]
    filename    = update.message.video.file_id + '.' + ext
    user        = update.message.from_user
    document    =  bot.get_file(update.message.video.file_id)
    document.download (filename)
    logger.info ("Got video from %s: %s", user.first_name, filename)
    update.message.reply_text (transfer (filename))

#   MAIN
def main ():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater ("409625517:AAEAtdlA14CyChi33KyLyILEowbij97IP88")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler (CommandHandler ("start",        cmd_start))
    dp.add_handler (CommandHandler ("help",         cmd_help))
    dp.add_handler (CommandHandler ("halt",         cmd_halt))

    # on unknown command, put some help text
    dp.add_handler (MessageHandler (Filters.command, cmd_unknown))

    # Add stuff to handle
    dp.add_handler (MessageHandler (Filters.audio,      fbk_audio))
    dp.add_handler (MessageHandler (Filters.video,      fbk_video))
    dp.add_handler (MessageHandler (Filters.document,   fbk_document))

    # log all errors
    dp.add_error_handler (cmd_error)

    # Start the Bot
    updater.start_polling ()
    logger.info ('Kicking')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling () is non-blocking and will stop the bot gracefully.
    updater.idle ()


if __name__ == '__main__':
    main ()

