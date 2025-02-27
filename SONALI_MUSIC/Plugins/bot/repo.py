from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI_MUSIC import app
from config import BOT_USERNAME
from SONALI_MUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """**
✪ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ˹ ᴠɪʟʟᴀɪɴ-ᴍᴜsɪᴄ ˼ ʙᴏᴛ ✪
 
 ❍ • ʙsᴅᴋ ʀᴇᴘᴏ ʟᴇɢᴀ ◉‿◉ •
 
 ❍ • ᴘᴇʜʟᴇ ᴠɪʟʟᴀɪɴ ᴋᴏ ᴘᴀᴘᴀ ʙᴏʟ •
 
 ❍ • ᴄʜᴜᴘ ᴄʜᴀᴘ ʙᴏᴛ ʟᴇᴋᴇ ɴɪᴋᴀʟ •
 
 ❍ • ʀᴇᴘᴏ ᴛᴏ ɴᴀʜɪ ᴍɪʟᴇɢᴀ ʙᴇᴛᴀ ⊂◉‿◉ •
 
 ❍ • ᴀɢʀ ʀᴇᴘᴏ ᴄʜᴀʜɪʏᴇ ᴛᴏ ᴠɪʟʟᴀɪɴ ᴋᴏ ᴘᴀᴘᴀ ʙᴏʟɴᴀ ᴘᴀᴅᴇɢᴀ •
 
 ❍ • ᴠɪʟʟᴀɪɴ ᴘᴀᴘᴀ • **"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("•ᴀᴅᴅ ᴍᴇ•", url=f"https://t.me/radha_music_bot?startgroup=true")
        ],
        [
          InlineKeyboardButton("•sᴜᴘᴘᴏʀᴛ•", url="https://t.me/oldskoolgc"),
          InlineKeyboardButton("•ᴏᴡɴᴇʀ•", url="https://t.me/iamakki001"),
          ],
               [
                InlineKeyboardButton("•ᴜᴘᴅᴀᴛᴇs•", url="https://t.me/iamvillain77"),

],
[
              InlineKeyboardButton("˹ʀᴧᴅʜᴧ ꭙ ᴍᴜꜱɪᴄ˼ ♪", url=f"https://t.me/radha_music_bot"),
              InlineKeyboardButton("︎˹ᴋᴜᴋᴜ ꭙ ᴍᴜꜱɪᴄ˼ ♪", url=f"https://t.me/Kuku_music_bot"),
              ],
              [
              InlineKeyboardButton("•sᴘᴏᴛɪғʏ ᴍᴜsɪᴄ•", url=f"https://t.me/Spotify_Muxic_bot"),
InlineKeyboardButton("˹ᴏᴅꜱ ꭙ ᴍᴜꜱɪᴄ˼ ♪", url=f"https://t.me/odsmusicbot"),
],
[
InlineKeyboardButton("˹ꜱɪʏᴧ ꭙ ᴍᴜꜱɪᴄ˼ ♪", url=f"https://t.me/siya_music_robot"),
InlineKeyboardButton("Ҩ፝֟፝ɴ┋ꕶʜɪᴢ֟፝ᴜᴋᴀ ♡", url=f"https://t.me/Shizuka_Chat_Robot"),
],
[
              InlineKeyboardButton("•ᴏʟᴅ ꜱᴋᴏᴏʟ ɢᴄ•", url=f"https://t.me/oldskoolgc"),
              InlineKeyboardButton("˹ᴠɪʟʟᴀɪɴ ꭙ ꜱᴜᴘᴘᴏʀᴛ˼", url=f"https://t.me/iamvillain77"),
              ],
              [
              InlineKeyboardButton("ᴀʟʟ ʙᴏᴛ", url=f"https://t.me/iamvillain77/62"),
        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://files.catbox.moe/pcncfx.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
 
   
# --------------


@app.on_message(filters.command("repo", prefixes="#"))
@capture_err
async def repo(_, message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/repos/BABY-MUSIC/BABYTUNE/contributors")
    
    if response.status_code == 200:
        users = response.json()
        list_of_users = ""
        count = 1
        for user in users:
            list_of_users += f"{count}. [{user['login']}]({user['html_url']})\n"
            count += 1

        text = f"""[•ʙᴏᴛ-ᴏᴡɴᴇʀ•](https://t.me/iamakki001) | [•ᴜᴘᴅᴀᴛᴇs•](https://t.me/iamvillain77)
| 𝖢𝖮𝖭𝖳𝖱𝖨𝖡𝖴𝖳𝖮𝖱𝖲 |
----------------
{list_of_users}"""
        await app.send_message(message.chat.id, text=text, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, text="Failed to fetch contributors.")
