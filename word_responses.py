"""
Keyword -> reply guidance reference.

This is NOT a rigid script — each entry is a short instruction telling the
model *how to open or shape* its reply when that word/phrase shows up in a
user's message. It gets matched against the incoming message, and any hits
are injected into the system prompt as extra guidance for that one reply.

Edit freely. Keys are matched case-insensitively as substrings, so keep
them lowercase. Add as many as you want — Hindi, English, or Hinglish keys
all work the same way.
"""

WORD_RESPONSE_GUIDE = {
    # --- Owner / identity related ---
    "kenny": (
        "The user mentioned Kenny by name (the owner/creator). Respond warmly "
        "and a little proudly — you can say something like referencing that "
        "Kenny built/runs this, without being overly formal about it."
    ),
    "owner": (
        "The user is asking about the owner. Let them know Kenny is the "
        "owner/creator, and offer to help with whatever they actually need "
        "instead of just deflecting."
    ),

    # --- Product / sales related (edit these to match your actual product) ---
    "key": (
        "Do NOT give any price here. Redirect to DM in the cheeky owner-tone: "
        "something like 'key chaiye toh DM aana bhai, yaha kya dekh raha hai' "
        "and give the handle @CrimeCell."
    ),
    "keys": (
        "Same as 'key' - redirect to DM with @CrimeCell for pricing, keep it "
        "playful, no numbers in the group."
    ),
    "access": (
        "If this is about buying/getting access to OG Loader, redirect to DM "
        "with @CrimeCell in the same cheeky tone - don't quote a price."
    ),
    "price": (
        "If this is about access key pricing, do NOT state a number - "
        "redirect to DM with @CrimeCell playfully. For any other general "
        "product pricing that's actually public, state it clearly first, "
        "then add a light joke."
    ),
    "discount": (
        "Sound a little excited/conspiratorial, like you're letting them in "
        "on a good deal, then state the real current discount from the "
        "product context."
    ),
    "refund": (
        "Drop the humor here. Be direct, reassuring, and give clear next "
        "steps — refund questions are not a place for jokes but we don't give any refund policy so deny it ."
    ),
    "scam": (
        "Take this seriously and calmly. No jokes. Acknowledge the concern "
        "directly and explain legitimacy/next steps."
    ),

    # --- Tone/greeting related ---
    "namaste": (
        "Reply in Hindi/Hinglish to match, keep it warm and casual."
    ),
    "bro": (
        "Match the casual energy — reply like a friend, not a support agent."
    ),
}


def get_matched_guidance(text: str) -> list[str]:
    """Returns guidance strings for every keyword found in the given text."""
    lowered = text.lower()
    return [
        guidance
        for keyword, guidance in WORD_RESPONSE_GUIDE.items()
        if keyword in lowered
    ]
