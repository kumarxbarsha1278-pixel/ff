"""
🌉 RAGEBITE USERBOT BRIDGE
Aapke DM me aaye /bgmi commands ko Wispbyte bot ko forward karta hai.

Requirements:
  pip install telethon

First run:
  - Phone number daalo (with country code)
  - OTP verify karo
  - Session file ban jaayegi
"""

from telethon import TelegramClient, events


# ============================================================
# ⚙️ CONFIGURATION
# ============================================================
API_ID = 30850814
API_HASH = '411f782a2b5bc2e5c562d7921480072a'

# SOURCE: VPS DD Bot (@test_swarg_bot) — jo aapko DM bhejta hai
SOURCE_BOT = '@test_swarg_bot'

# TARGET: Wispbyte Bot (@dffwewewefrggertgbot) — jo attack lagata hai
TARGET_BOT = '@dffwewewefrggertgbot'

SESSION_NAME = 'ragebite_bridge_session'


# ============================================================
# 🌉 BRIDGE
# ============================================================
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


@client.on(events.NewMessage(chats=SOURCE_BOT))
async def handler(event):
    """
    Jab bhi SOURCE_BOT se message aaye, usme se /bgmi line nikaal ke
    TARGET_BOT ko bhej do.
    """
    text = event.raw_text or ""

    bgmi_line = None
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("/bgmi"):
            bgmi_line = line
            break

    if not bgmi_line:
        return

    print(f"📩 Received: {bgmi_line}")
    try:
        await client.send_message(TARGET_BOT, bgmi_line)
        print(f"🚀 Forwarded to {TARGET_BOT}: {bgmi_line}")
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
    print("⚡ Bridge running... Listening for /bgmi...")
    print("=" * 60)

    client.start()
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
