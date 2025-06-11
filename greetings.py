# Ultroid - UserBot
# Copyright (C) 2021-2025 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

---- Welcomes ----
• `{i}setwelcome <message/reply to message>`
    Set welcome message in the current chat.

• `{i}clearwelcome`
    Delete the welcome in the current chat.

• `{i}getwelcome`
    Get the welcome message in the current chat.

---- GoodByes ----
• `{i}setgoodbye <message/reply to message>`
    Set goodbye message in the current chat.

• `{i}cleargoodbye`
    Delete the goodbye in the current chat.

• `{i}getgoodbye`
    Get the goodbye message in the current chat.

• `{i}thankmembers on/off`
    Send a thank you sticker on hitting a members count of 100*x in your groups.
"""
import os

from . import upload_file as uf
from telethon.utils import pack_bot_file_id

from pyUltroid.fns.tools import create_tl_btn, format_btn, get_msg_button

from . import HNDLR, eor, get_string, mediainfo, udB, ultroid_cmd
from ._inline import something

# Functions moved from greetings_db.py
def get_stuff(key=None):
    return udB.get_key(key) or {}


def add_welcome(chat, msg, media, button):
    ok = get_stuff("WELCOME")
    ok.update({chat: {"welcome": msg, "media": media, "button": button}})
    return udB.set_key("WELCOME", ok)


def get_welcome(chat):
    ok = get_stuff("WELCOME")
    return ok.get(chat)


def delete_welcome(chat):
    ok = get_stuff("WELCOME")
    if ok.get(chat):
        ok.pop(chat)
        return udB.set_key("WELCOME", ok)


def add_goodbye(chat, msg, media, button):
    ok = get_stuff("GOODBYE")
    ok.update({chat: {"goodbye": msg, "media": media, "button": button}})
    return udB.set_key("GOODBYE", ok)


def get_goodbye(chat):
    ok = get_stuff("GOODBYE")
    return ok.get(chat)


def delete_goodbye(chat):
    ok = get_stuff("GOODBYE")
    if ok.get(chat):
        ok.pop(chat)
        return udB.set_key("GOODBYE", ok)


def add_thanks(chat):
    x = get_stuff("THANK_MEMBERS")
    x.update({chat: True})
    return udB.set_key("THANK_MEMBERS", x)


def remove_thanks(chat):
    x = get_stuff("THANK_MEMBERS")
    if x.get(chat):
        x.pop(chat)
        return udB.set_key("THANK_MEMBERS", x)


def must_thank(chat):
    x = get_stuff("THANK_MEMBERS")
    return x.get(chat)


Note = "\n\nNote: `{mention}`, `{group}`, `{count}`, `{name}`, `{fullname}`, `{username}`, `{userid}` can be used as formatting parameters.\n\n"


@ultroid_cmd(pattern="setwelcome", groups_only=True)
async def setwel(event):
    x = await event.eor(get_string("com_1"))
    r = await event.get_reply_message()
    btn = format_btn(r.buttons) if (r and r.buttons) else None
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        text = r.text if r else None
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await r.download_media()
            m = uf(dl)
            os.remove(dl)
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eor(x, get_string("com_4"), time=5)
            dl = await r.download_media()
            m = uf(dl)
            os.remove(dl)
        elif wut == "web":
            m = None
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            txt = r.text
            if not btn:
                txt, btn = get_msg_button(r.text)
            add_welcome(event.chat_id, txt, m, btn)
        else:
            add_welcome(event.chat_id, None, m, btn)
        await eor(x, get_string("grt_1"))
    elif text:
        if not btn:
            txt, btn = get_msg_button(text)
        add_welcome(event.chat_id, txt, None, btn)
        await eor(x, get_string("grt_1"))
    else:
        await eor(x, get_string("grt_3"), time=5)


@ultroid_cmd(pattern="clearwelcome$", groups_only=True)
async def clearwel(event):
    if not get_welcome(event.chat_id):
        return await event.eor(get_string("grt_4"), time=5)
    delete_welcome(event.chat_id)
    await event.eor(get_string("grt_5"), time=5)


@ultroid_cmd(pattern="getwelcome$", groups_only=True)
async def listwel(event):
    wel = get_welcome(event.chat_id)
    if not wel:
        return await event.eor(get_string("grt_4"), time=5)
    msgg, med = wel["welcome"], wel["media"]
    if wel.get("button"):
        btn = create_tl_btn(wel["button"])
        return await something(event, msgg, med, btn)
    await event.reply(f"**Welcome Note in this chat**\n\n`{msgg}`", file=med)
    await event.delete()


@ultroid_cmd(pattern="setgoodbye", groups_only=True)
async def setgb(event):
    x = await event.eor(get_string("com_1"))
    r = await event.get_reply_message()
    btn = format_btn(r.buttons) if (r and r.buttons) else None
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        text = r.text if r else None
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await r.download_media()
            m = uf(dl)
            os.remove(dl)
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eor(x, get_string("com_4"), time=5)
            dl = await r.download_media()
            m = uf(dl)
            os.remove(dl)
        elif wut == "web":
            m = None
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            txt = r.text
            if not btn:
                txt, btn = get_msg_button(r.text)
            add_goodbye(event.chat_id, txt, m, btn)
        else:
            add_goodbye(event.chat_id, None, m, btn)
        await eor(x, "`Goodbye note saved`")
    elif text:
        if not btn:
            txt, btn = get_msg_button(text)
        add_goodbye(event.chat_id, txt, None, btn)
        await eor(x, "`Goodbye note saved`")
    else:
        await eor(x, get_string("grt_7"), time=5)


@ultroid_cmd(pattern="cleargoodbye$", groups_only=True)
async def clearwgb(event):
    if not get_goodbye(event.chat_id):
        return await event.eor(get_string("grt_6"), time=5)
    delete_goodbye(event.chat_id)
    await event.eor("`Goodbye Note Deleted`", time=5)


@ultroid_cmd(pattern="getgoodbye$", groups_only=True)
async def listgd(event):
    wel = get_goodbye(event.chat_id)
    if not wel:
        return await event.eor(get_string("grt_6"), time=5)
    msgg = wel["goodbye"]
    med = wel["media"]
    if wel.get("button"):
        btn = create_tl_btn(wel["button"])
        return await something(event, msgg, med, btn)
    await event.reply(f"**Goodbye Note in this chat**\n\n`{msgg}`", file=med)
    await event.delete()


@ultroid_cmd(pattern="thankmembers (on|off)", groups_only=True)
async def thank_set(event):
    type_ = event.pattern_match.group(1).strip()
    if not type_ or type_ == "":
        await eor(
            event,
            f"**Current Chat Settings:**\n**Thanking Members:** `{must_thank(event.chat_id)}`\n\nUse `{HNDLR}thankmembers on` or `{HNDLR}thankmembers off` to toggle current settings!",
        )
        return
    chat = event.chat_id
    if type_.lower() == "on":
        add_thanks(chat)
    elif type_.lower() == "off":
        remove_thanks(chat)
    await eor(
        event,
        f"**Done! Thank you members has been turned** `{type_.lower()}` **for this chat**!",
    )
