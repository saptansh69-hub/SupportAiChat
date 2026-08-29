# Telegram Product Assistant Bot

A standalone bot (separate from your website codebase) that answers product
and pricing questions in Telegram groups/channels, moderates spam, and
replies in English or Hindi automatically.

## Important reality check

This runs as its own **bot account** via BotFather — Telegram bots can't
post *as your personal account*. That's actually a good thing: automating
a real personal account (a "userbot") violates Telegram's terms and risks
a ban. This bot just needs its own name/avatar and admin rights in your
group, and it'll function as your assistant just fine.

## 1. Create the bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`
2. Save the token it gives you → this is `TELEGRAM_TOKEN`
3. Add the bot to your group/channel and promote it to **admin** (needed
   for deleting messages and muting spammers)

## 2. Get a Gemini API key

Create one at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
→ this is `GEMINI_API_KEY`. The default model is `gemini-2.0-flash` (fast +
cheap, good for chat); change `GEMINI_MODEL` in `.env` if you want a
different one.

## 3. Point it at your product data

Fill in **one** of:
- `WEBSITE_API_URL` — if your existing backend has JSON endpoints like
  `/products` and `/pricing`, use this. Fastest and most reliable.
- `WEBSITE_URL` — plain website URL. The bot will scrape the visible text
  as a fallback if you don't have an API.

## 4. Set the personality

Edit `BOT_PERSONALITY` in `config.py` (or as an env var). Describe tone,
humor style, how casual/formal it should be, and that it should mirror
Hindi/English/Hinglish depending on what the user writes. This is the
single biggest lever for how the bot "feels."

## 5. Run locally (in Codespaces)

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your values
export $(cat .env | xargs)   # or use a .env loader
python bot.py
```

## 6. Deploy on Railway (separate project from your website)

1. Push this folder to a **new** GitHub repo (not your existing one)
2. Create a new Railway project → deploy from that repo
3. Add all variables from `.env.example` in Railway's Variables tab
4. Railway will pick up `nixpacks.toml` automatically and run `python bot.py`

## What it does out of the box

- **Answers questions** about product/pricing in DMs always, and in groups
  when mentioned, replied to, or asked something pricing/product-related
- **Refreshes product info** from your website every 30 min (configurable)
  so it never goes stale
- **Moderates spam**: deletes messages matching banned patterns
  (`config.BANNED_PATTERNS`), and auto-mutes anyone flooding the chat
  (more than N messages in a short window — tune in `config.py`)
- **Bilingual**: Claude replies in whichever language the user wrote in

## Where to extend

- `config.py` — personality, thresholds, banned patterns, admin IDs
- `word_responses.py` — keyword → reply-guidance reference (see below)
- `knowledge.py` — how product data is fetched (swap in your real API shape)
- `handlers/moderation.py` — add more spam rules
- `handlers/commands.py` — add more slash commands

## Word-response reference (`word_responses.py`)

This file is a lookup table: specific words/phrases → a short instruction
on *how* the bot should open or shape its reply when that word shows up.
It's not a scripted canned-reply system — the model still writes the
actual sentence — this just steers it.

Two entries are already in there for "kenny" and "owner" so the bot always
reacts warmly whenever either is mentioned, anywhere in a message, even
without a question mark or other trigger.

```python
"kenny": (
    "The user mentioned Kenny by name (the owner/creator). Respond warmly "
    "and a little proudly..."
),
```

Add as many keyword → guidance pairs as you want — pricing terms, product
names, common complaints, whatever comes up in your group. Keys are
matched as lowercase substrings, so "kenny" also matches "hey kenny" or
"kennys the best".
