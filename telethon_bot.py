import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import smtplib
from email.mime.text import MIMEText

# ✅ متغيرات البيئة
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
sender_email = os.getenv("EMAIL_SENDER")
app_password = os.getenv("EMAIL_PASS")
recipient_email = os.getenv("EMAIL_RECEIVER")
session_name = "moomen_session_v3"  # ← اسم جديد للجلسة

# ✅ تابع إرسال الإيميل
def send_email_alert(subject, body):
    msg = MIMEText(body, _charset="utf-8")
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("📧 Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ✅ عميل التليجرام
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    sender = await event.get_sender()
    name = sender.first_name if sender else "شخص مجهول"
    message_text = event.raw_text.lower()

    if any(word in message_text for word in ["هام", "عاجل", "ضروري"]):
        send_email_alert(
            subject="📌 رسالة تليجرام مهمة",
            body=f"المرسل: {name}\n\nالرسالة:\n{event.raw_text}"
        )
        await event.reply("📌 تم استلام رسالتك الهامة، هبلّغ مؤمن فورًا إن شاء الله.")
        print(f"🚨 رسالة مهمة من {name}: {event.raw_text}")
    else:
        print(f"📩 رسالة من {name}: {event.raw_text}")

# ✅ تشغيل البوت
print("🤖 جاري تشغيل البوت من رقمك...")
async def main():
    await client.start()
    print("✅ البوت شغال دلوقتي. مستني الرسائل...")
    await client.run_until_disconnected()

asyncio.run(main())
