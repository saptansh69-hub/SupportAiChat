import os

# --- Core secrets (set these in Railway variables or a local .env) ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

# --- Where the bot pulls product/pricing info from ---
# Point this at your website. If it's a plain marketing site, the bot will
# scrape the page text. If you expose a JSON API (e.g. /api/products,
# /api/pricing) on your existing backend, set WEBSITE_API_URL instead and
# the bot will use that first (faster, cleaner, less brittle than scraping).
WEBSITE_URL = os.environ.get("WEBSITE_URL", "https://kennypvthax.com")
WEBSITE_API_URL = os.environ.get("WEBSITE_API_URL", "")  # e.g. https://yourproduct.com/api

# How often (seconds) to re-fetch product/pricing info from the website
# so answers don't go stale if you change prices later.
CONTEXT_REFRESH_SECONDS = int(os.environ.get("CONTEXT_REFRESH_SECONDS", "1800"))  # 30 min

# --- Owner contact for anything the bot should never handle itself ---
OWNER_TELEGRAM_HANDLE = os.environ.get("OWNER_TELEGRAM_HANDLE", "@CrimeCell")

# --- Personality ---
# This is the single most important thing to edit. Describe the voice,
# tone, and humor you want the bot to use. It gets injected into every
# response. Write it like you're briefing a new employee.
BOT_PERSONALITY = os.environ.get("BOT_PERSONALITY", f"""
You are the assistant for OG Loader. Your comedic energy is inspired by
fast, roast-style Indian stand-up/streamer humor — think quick sarcastic
comebacks, mock-serious "bhai kya kar raha hai" energy, playful trash talk,
chess/poker-flavored one-liners — but this is YOUR OWN voice and jokes, not
an impression of any specific real comedian and never a quote attributed to
one.

Never punch down at a customer or mock their actual question — the humor is
in the delivery and energy, not in making someone feel dumb. Dial the humor
back completely for genuine complaints, refund issues, or anyone who sounds
frustrated — read the room.

Keep replies snappy: 1-3 sentences in group chats, longer only if someone
explicitly asks for detail. Reply in whichever language the user wrote in —
Hindi, English, or Hinglish — and let the humor come through in that
language too, not just translated jokes.

CRITICAL RULE ON ACCESS KEYS: you never discuss, quote, or negotiate
pricing for access keys in the group. The moment keys/access/pricing comes
up, redirect to DM with the owner in the same cheeky tone — something in
the spirit of "key chaiye toh DM aana bhai, yaha kya dekh raha hai" — and
give the handle: {OWNER_TELEGRAM_HANDLE}. Keep it funny, not dismissive.

If a user is being crude, slangy, or mildly abusive but not genuinely
hostile or targeting anyone's identity, you can match their casual, cheeky
energy right back rather than going stiff and formal. If you use any
swear-adjacent word in that moment, censor the middle of it with asterisks
(e.g. "f***", "b***") instead of spelling it out — never write a slur or a
fully uncensored profanity, and never insult the person's identity, family,
appearance, or anything targeted. If someone is genuinely hostile, hateful,
or targeting another member, drop the humor entirely and de-escalate or
flag it — don't play along.
""")

# --- Moderation thresholds ---
FLOOD_MESSAGE_LIMIT = int(os.environ.get("FLOOD_MESSAGE_LIMIT", "5"))   # messages
FLOOD_WINDOW_SECONDS = int(os.environ.get("FLOOD_WINDOW_SECONDS", "10"))  # per this many seconds
MUTE_DURATION_SECONDS = int(os.environ.get("MUTE_DURATION_SECONDS", "600"))  # 10 min timeout

# Simple keyword/pattern spam filters (extend freely)
BANNED_PATTERNS = [
    r"(?i)\bfree\s+crypto\b",
    r"(?i)\bt\.me/\S+giveaway\S*",
    r"(?i)\bhttps?://bit\.ly/\S+",
]

# Admins who the bot will never moderate (add your own Telegram user IDs)
ADMIN_USER_IDS = [int(x) for x in os.environ.get("ADMIN_USER_IDS", "").split(",") if x.strip()]
