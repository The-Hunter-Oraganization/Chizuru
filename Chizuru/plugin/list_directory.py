from pySmartDL import SmartDL
import io, sys, traceback, os, re, subprocess, asyncio, requests, time
from datetime import datetime as dt
from natsort import natsorted
from pyrogram import Client, filters
from pathlib import Path
import importlib
import shlex
from os.path import basename, join, exists
from typing import Tuple, List, Optional, Iterator, Union, Any
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from Chizuru import pbot as sohailpyro, OWNER as OWNER_ID, TRIGGERS as trg, UTRIGGERS
from Chizuru.utils.decorators import send_msg_or_document_text
from Chizuru.database.authorize import is_auth
_PTN_SPLIT = re.compile(r'(\.\d+|\.|\d+)')

def humanbytes(size: float) -> str:
    """ humanize size """
    if not size:
        return "0 B"
    power = 1024
    t_n = 0
    power_dict = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti', 5: 'Pi', 6: 'Ei', 7: 'Zi', 8: 'Yi'}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])

def _sort_algo(data: List[str]) -> Iterator[Union[str, float]]:
    """ sort algo for file names """
    p1 = 0.0
    for p2 in data:
        # skipping null values
        if not p2:
            continue

        # first letter of the part
        c = p2[0]

        # checking c is a digit or not
        # if yes, p2 should not contain any non digits
        if c.isdigit():
            # p2 should be [0-9]+
            # so c should be 0-9
            if c == '0':
                # add padding
                # this fixes `a1` and `a01` messing
                if isinstance(p1, str):
                    yield 0.0
                yield c

            # converting to float
            p2 = float(p2)

            # add padding
            if isinstance(p1, float):
                yield ''

        # checking p2 is `.[0-9]+` or not
        elif c == '.' and len(p2) > 1 and p2[1].isdigit():
            # p2 should be `.[0-9]+`
            # so converting to float
            p2 = float(p2)

            # add padding
            if isinstance(p1, str):
                yield 0.0
            yield c

        # add padding if previous and current both are strings
        if isinstance(p1, str) and isinstance(p2, str):
            yield 0.0

        yield p2
        # saving current value for later use
        p1 = p2

def sort_file_name_key(file_name: str) -> tuple:
    """ sort key for file names """
    if not isinstance(file_name, str):
        file_name = str(file_name)
    return tuple(_sort_algo(_PTN_SPLIT.split(file_name.lower())))
 
@sohailpyro.on_message(filters.command('ls', prefixes=trg))
async def download_(client: sohailpyro, message: Message):
    check = is_auth(message.from_user.id) 
    if check is False:
        await message.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]
    if not exists(cmd):
        await message.reply("path not exists!")
        return
    path_ = Path(cmd)
    out = f"<b>PATH</b> : <code>{cmd}</code>\n\n"
    if path_.is_dir():
        folders = ''
        files = ''
        for p_s in sorted(path_.iterdir(), key=lambda a: sort_file_name_key(a.name)):
            if p_s.is_file():
                if str(p_s).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += '🎵'
                elif str(p_s).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
                    files += '📹'
                elif str(p_s).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += '🗜'
                elif str(p_s).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")):
                    files += '🖼'
                else:
                    files += '📄'
                size = os.stat(str(p_s)).st_size
                files += f" <code>{p_s.name}</code> <i>({humanbytes(size)})</i>\n"
            else:
                folders += f"📁 <code>{p_s.name}</code>\n"
        out += (folders + files) or "<code>empty path!</code>"   
        await status_message.delete()
        await send_msg_or_document_text(out, message)  
    else:
        size = os.stat(str(path_)).st_size
        out += f"📄 <code>{path_.name}</code> <i>({humanbytes(size)})</i>\n"
        await send_msg_or_document_text(out, message) 
    
        
