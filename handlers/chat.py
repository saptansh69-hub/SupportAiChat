import google.generativeai as genai
from telegram import Update
from telegram.ext import ContextTypes

import config
import knowledge
from word_responses import get_matched_guidance

genai.configure(api_key=config.GEMINI_API_KEY)

# Widened trigger list so the bot jumps in eagerly rather than needing an
# exact keyword match - a "responsive" bot should err toward replying.
# "kenny" and "owner" are included so the bot always reacts when its
# owner is mentioned.
TRIGGER_WORDS = [
    "price", "pricing", "cost", "buy", "product", "kitna", "kaisa hai",
    "kya hai", "features", "discount", "sale", "offer", "kaise", "kab",
    "available", "kharido", "paisa", "rupay", "kitne ka",
    "kenny", "owner", "key", "keys", "access", "unlock",
]


def _should_respond(update: Update) -> bool:
    chat_type = update.effective_chat.type
    if chat_type == "private":
        return True

    text = (update.message.text or "").lower()
    bot_username = update.get_bot().username or ""
    mentioned = f"@{bot_username.lower()}" in text
    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.is_bot
    )
    keyword_hit = any(w in text for w in TRIGGER_WORDS)
    is_question = "?" in text  # jump into questions even without a keyword match
    return mentioned or is_reply_to_bot or keyword_hit or is_question


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if not _should_respond(update):
        return

    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    product_context = knowledge.get_product_context()

    matched_guidance = get_matched_guidance(user_text)
    guidance_block = ""
    if matched_guidance:
        guidance_block = "\nSpecific guidance for this message (from the word-response reference):\n" + \
            "\n".join(f"- {g}" for g in matched_guidance)

    system_prompt = f"""{config.BOT_PERSONALITY}

Here is the latest product & pricing information, pulled live from the
website. Only use this for facts - never invent prices or features that
aren't here:

{product_context}
{guidance_block}
"""

    try:
        model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            system_instruction=system_prompt,
        )
        response = model.generate_content(user_text)
        reply = response.text
    except Exception as e:
        reply = "Systam hang hogya bccc ."
        print(f"Chud Gye guru 😭: {e}")

    await update.message.reply_text(reply)
