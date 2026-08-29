from telegram import Update
from telegram.ext import ContextTypes

import knowledge


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! Mai Owner ka sevak hu vo toh sorha hai bta kya kaam tha mai madad krdeta hu  English ya Hindi, dono samjh leta hu tu bindaas puch bhai 😸"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/price — latest pricing\n"
        "/products — what we offer\n"
        "Or just ask me naturally in the chat, mention me, or reply to one "
        "of my messages."
    )


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = knowledge.get_product_context()
    await update.message.reply_text(f"ye le lawde latest news :\n\n{info[:1500]}")
