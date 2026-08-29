import re
import time
from collections import defaultdict, deque

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

import config

# user_id -> deque of recent message timestamps, per chat
_recent_messages = defaultdict(lambda: defaultdict(deque))

_compiled_patterns = [re.compile(p) for p in config.BANNED_PATTERNS]


async def _mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    until = int(time.time()) + config.MUTE_DURATION_SECONDS
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=until,
    )


async def moderate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Run before chat handling. Deletes spam / flood, mutes repeat offenders."""
    if not update.message or not update.effective_user:
        return False  # not moderated, let other handlers proceed

    user = update.effective_user
    if user.id in config.ADMIN_USER_IDS or user.is_bot:
        return False

    chat_id = update.effective_chat.id
    text = update.message.text or update.message.caption or ""

    # 1. Banned pattern check (known spam/scam formats)
    if any(p.search(text) for p in _compiled_patterns):
        await _delete_and_warn(update, context, user.id, reason="spam link/pattern detected")
        return True

    # 2. Flood check (too many messages too fast)
    now = time.time()
    dq = _recent_messages[chat_id][user.id]
    dq.append(now)
    while dq and now - dq[0] > config.FLOOD_WINDOW_SECONDS:
        dq.popleft()

    if len(dq) > config.FLOOD_MESSAGE_LIMIT:
        await _delete_and_warn(update, context, user.id, reason="flooding the chat")
        await _mute_user(update, context, user.id)
        dq.clear()
        return True

    return False


async def _delete_and_warn(update, context, user_id, reason: str):
    try:
        await update.message.delete()
    except Exception as e:
        print(f"Could not delete message: {e}")
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ Removed a message from a member for: {reason}.",
        )
    except Exception as e:
        print(f"Could not send warning: {e}")
