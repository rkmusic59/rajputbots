import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from SONALI_MUSIC import app  # Assuming this is the app instance from your project

@app.on_message(filters.command("ask"))
async def fetch_med_info(client, message):
    query = " ".join(message.command[1:])  # Extract the query after the command
    if not query:
        await message.reply_text("**ᴘʟᴇᴀsᴇ ᴘʀᴘᴠɪᴅᴇ ᴀ ǫᴜᴇʀʏ ᴛᴏ ᴀsᴋ**.")
        return

    # Send typing action to indicate bot is working
    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Use the API to get medical data
    api_url = f"https://chatwithai.codesearch.workers.dev/?chat={query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("data", "**sᴏʀʀʏ, ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғᴇᴛᴄʜ ᴛʜᴇ ᴅᴀᴛᴀ.**")
        else:
            reply = "**ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴅᴀᴛᴀ ғʀᴏᴍ ᴛʜᴇ ᴀᴘɪ.**"
    except Exception as e:
        reply = f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :** {e}"

    # Add attribution and reply to the user
    reply += "\n\n**❍ ᴀɴsᴡᴇʀ ʙʏ :- @Sonali_Music_Bot**"
    await message.reply_text(reply)

@app.on_message(filters.mentioned & filters.group)
async def fetch_med_info_group(client, message):
    query = " ".join(message.command[1:])  # Extract the query after the command
    if not query:
        await message.reply_text("**ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇᴅɪᴄᴀʟ ǫᴜᴇʀʏ ᴛᴏ ᴀsᴋ.**")
        return

    # Send typing action to indicate bot is working
    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Use the API to get medical data
    api_url = f"https://chatwithai.codesearch.workers.dev/?chat={query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("data", "**sᴏʀʀʏ, ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғᴇᴛᴄʜ ᴛʜᴇ ᴅᴀᴛᴀ.**")
        else:
            reply = "**ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴅᴀᴛᴀ ғʀᴏᴍ ᴛʜᴇ ᴀᴘɪ.**"
    except Exception as e:
        reply = f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :** {e}"

    # Add attribution and reply to the user
    reply += "\n\n**❍ ᴀɴsᴡᴇʀ ʙʏ :- @Sonali_Music_Bot**"
    await message.reply_text(reply)
