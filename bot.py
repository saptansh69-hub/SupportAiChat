import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

import config
from handlers import commands, chat, moderation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def message_router(update, context):
    """Moderation runs first; if it deletes the message, we stop there."""
    moderated = await moderation.moderate_message(update, context)
    if moderated:
        return
    await chat.handle_message(update, context)


def main():
    if not config.TELEGRAM_TOKEN:
        raise SystemExit("TELEGRAM_TOKEN is not set. Add it in Railway variables or .env")
    if not config.GEMINI_API_KEY:
        raise SystemExit("GEMINI_API_KEY is not set. Add it in Railway variables or .env")

    app = Application.builder().token(config.TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", commands.start_command))
    app.add_handler(CommandHandler("help", commands.help_command))
    app.add_handler(CommandHandler("price", commands.price_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
