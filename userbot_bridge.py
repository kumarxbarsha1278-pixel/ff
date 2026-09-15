"""
🌉 RAGEBITE USERBOT BRIDGE
Sirf /bgmi commands forward karta hai (details ignore karta hai)
"""

from telethon import TelegramClient, events


# ============================================================
# ⚙️ CONFIGURATION
# ============================================================
API_ID = 30850814
API_HASH = '411f782a2b5bc2e5c562d7921480072a'

# SOURCE: DD Bot (@test_swarg_bot) — jo aapko DM bhejta hai
SOURCE_BOT = '@test_swarg_bot'

# TARGET: MAIN Bot (@maIN_SWARGBOT) — jo attack lagayega
TARGET_BOT = '@maIN_SWARGBOT'

SESSION_NAME = 'ragebite_bridge_session'


# ============================================================
# 🌉 BRIDGE
# ============================================================
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


@client.on(events.NewMessage(chats=SOURCE_BOT))
async def handler(event):
    """
    Sirf /bgmi commands forward karo.
    Details wale messages ignore karo.
    """
    text = (event.raw_text or "").strip()

    # Sirf /bgmi se start hone wale messages forward karo
    if not text.startswith("/bgmi"):
        print(f"⏭️ Ignored (not /bgmi): {text[:50]}")
        return

    print(f"📩 Command received: {text}")
    try:
        await client.send_message(TARGET_BOT, text)
        print(f"🚀 Forwarded to {TARGET_BOT}: {text}")
    except Exception as e:
        print(f"❌ Forward failed: {e}")


# ============================================================
# 🚀 MAIN
# ============================================================
def main():
    print("=" * 60)
    print("🌉 RAGEBITE USERBOT BRIDGE")
    print("=" * 60)
    print(f"📥 Source: {SOURCE_BOT}")
    print(f"📤 Target: {TARGET_BOT}")
    print("=" * 60)
    print("⚡ Bridge running... Listening for /bgmi only...")
    print("=" * 60)

    client.start()
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
