import imghdr
import os
from asyncio import gather
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from SONALI_MUSIC import app
from config import BOT_USERNAME
from SONALI_MUSIC.utils.errors import capture_err

from SONALI_MUSIC.utils.files import (
    get_document_from_file_id,
    resize_file_to_sticker_size,
    upload_document,
)

from SONALI_MUSIC.utils.stickerset import (
    add_sticker_to_set,
    create_sticker,
    create_sticker_set,
    get_sticker_set_by_name,
)

# -----------

MAX_STICKERS = (
    120  # would be better if we could fetch this limit directly from telegram
)
SUPPORTED_TYPES = ["jpeg", "png", "webp"]
# ------------------------------------------
                    await bot.send_read_acknowledge(conv.chat_id)

            await args.edit(
                f"Sticker added! Your pack can be found [here](t.me/addstickers/{packname})",
                parse_mode='md'
            )


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image

@register(outgoing=True, pattern="^.stkrinfo$")
async def get_pack_info(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if not event.is_reply:
            await bot.update_message(event, PACKINFO_HELP)
            return
        rep_msg = await event.get_reply_message()
        if not rep_msg.document:
            await bot.update_message(event, "`Reply to a sticker to get the pack details`")
            return
        stickerset_attr = rep_msg.document.attributes[1]
        if not isinstance(stickerset_attr, DocumentAttributeSticker):
            await bot.update_message(event, "`Not a valid sticker`")
            return
        get_stickerset = await bot(GetStickerSetRequest(InputStickerSetID(id=stickerset_attr.stickerset.id, access_hash=stickerset_attr.stickerset.access_hash)))
        pack_emojis = []
        for document_sticker in get_stickerset.packs:
            if document_sticker.emoticon not in pack_emojis:
                pack_emojis.append(document_sticker.emoticon)
        OUTPUT = f"**Sticker Title:** `{get_stickerset.set.title}\n`" \
                f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n" \
                f"**Official:** `{get_stickerset.set.official}`\n" \
                f"**Archived:** `{get_stickerset.set.archived}`\n" \
                f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n" \
                f"**Emojis In Pack:** {' '.join(pack_emojis)}"
        await event.edit(OUTPUT)

CMD_HELP.update({
    "stickers": ".kang\
\nUsage: Reply .kang to a sticker or an image to kang it to your userbot pack.\
\n\n.kang [emoji('s)]\
\nUsage: Works just like .kang but uses the emoji('s) you picked.\
\n\n.kang [number]\
\nUsage: Kang's the sticker/image to the specified pack but uses 🤔 as emoji.\
\n\n.kang [emoji('s)] [number]\
\nUsage: Kang's the sticker/image to the specified pack and uses the emoji('s) you picked.\
\n\n.stkrinfo\
\nUsage: Gets info about the sticker pack."
})
