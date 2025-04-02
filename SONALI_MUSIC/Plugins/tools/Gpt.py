import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from SONALI_MUSIC import app  # बॉट का एप्लिकेशन इंपोर्ट करें

@app.on_message(filters.command("ai"))
async def fetch_med_info(client, message):
    YourQuery = " ".join(message.command[1:]) if len(message.command) > 1 else None  # YourQuery डिफाइन किया
    if not YourQuery:
        await message.reply_text("**ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ǫᴜᴇʀʏ ᴛᴏ ᴀsᴋ.**")
        return

    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    api_url = f"https://chatwithai.codesearchdev.workers.dev/?chat={YourQuery}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("data", "**sᴏʀʀʏ, ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғᴇᴛᴄʜ ᴛʜᴇ ᴅᴀᴛᴀ.**")
        else:
            reply = "**ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴅᴀᴛᴀ ғʀᴏᴍ ᴛʜᴇ ᴀᴘɪ.**"
    except Exception as e:
        reply = f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :** {e}"

    reply += "\n\n**❍ ᴀɴsᴡᴇʀ ʙʏ :- @radha_music_bot**"
    await message.reply_text(reply)

@app.on_message(filters.mentioned & filters.group)
async def fetch_med_info_group(client, message):
    YourQuery = message.text.replace(f"@{client.me.username}", "").strip()  # YourQuery डिफाइन किया
    if not YourQuery:
        await message.reply_text("**ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ǫᴜᴇʀʏ ᴛᴏ ᴀsᴋ.**")
        return

    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    api_url = f"https://chatwithai.codesearchdev.workers.dev/?chat={YourQuery}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("data", "**sᴏʀʀʏ, ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғᴇᴛᴄʜ ᴛʜᴇ ᴅᴀᴛᴀ.**")
        else:
            reply = "**ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴅᴀᴛᴀ ғʀᴏᴍ ᴛʜᴇ ᴀᴘɪ.**"
    except Exception as e:
        reply = f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :** {e}"

    reply += "\n\n**❍ ᴀɴsᴡᴇʀ ʙʏ :- @radha_music_bot**"
    await message.reply_text(reply)
