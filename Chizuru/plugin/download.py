from pySmartDL import SmartDL
import io, sys, traceback, os, re, subprocess, asyncio, requests, time, random
from datetime import datetime as dt
from natsort import natsorted
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from Chizuru.database.authorize import is_auth
from Chizuru import pbot, OWNER as OWNER_ID, TRIGGERS as trg
from Chizuru.utils.progress import progress_for_pyrogram

@pbot.on_message(filters.command('download', prefixes=trg))
async def download_(client: Client, message: Message):
    check = is_auth(message.from_user.id) 
    if check is False:
        await message.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    status_message = await message.reply_text("Processing ...")
    raw_msg = message.text.split(" ", maxsplit=1)[1]
    cmd = message.text.split(" ", maxsplit=1)[1]
    if '|' in cmd: 
        link = cmd.split('|', 1)
        cmd = link[0]
        filename = link[1]
    dest = './downloads/'
    obj = SmartDL(cmd,dest=dest, progress_bar=False)
    obj.start(blocking=False)
    destination = obj.get_dest()
    C_TIME = time.time()
    while not obj.isFinished():
        msgd = "Speed: %s" % obj.get_speed(human=True)
        msgd += "\nAlready downloaded: %s" % obj.get_dl_size(human=True)
        msgd += "\nEta: %s" % obj.get_eta(human=True)
        msgd += "\nProgress: %d%%" % (obj.get_progress()*100)
        msgd += "\nProgress bar: %s" % obj.get_progress_bar()
        msgd += "\nStatus: %s" % obj.get_status()
        time.sleep(0.2)
        try:
            await status_message.edit(msgd)
            time.sleep(5)
        except:
            print("Same Message")   
        
    if obj.isSuccessful():
        msgd = f"downloaded file to `{destination}`"
        msgd += "\n\ndownload task took %ss" % obj.get_dl_time(human=True) 
        if os.path.isfile(destination) is True:
            if '|' in raw_msg:
                try:
                    await message.reply_document(destination, thumb=f'downloads/thumb{message.from_user.id}.png',file_name=filename, progress=progress_for_pyrogram, progress_args=("**Uploadding.....** \n",status_message, C_TIME))
                    os.remove(destination)
                except:  
                    await message.reply(text='Error While File Uploading')   
            else:    
                try:
                    await message.reply_document(destination, thumb=f'downloads/thumb{message.from_user.id}.png', progress=progress_for_pyrogram, progress_args=("**Uploadding.....** \n",status_message, C_TIME))
                    os.remove(destination)
                except:
                    await message.reply(text='Error While File Uploading')    
        try:
            await status_message.edit(msgd)
            time.sleep(5)
        except:
            print("Same Message")    
    else:
        msgd = "There were some errors:"
        for e in obj.get_errors():
                msgd = str(e)   
                try:
                    await status_message.edit(msgd)
                    time.sleep(5)
                except:
                    print("Same Message")    
                    

        