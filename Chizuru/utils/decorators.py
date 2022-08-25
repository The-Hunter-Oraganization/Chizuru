import os
from sys import prefix
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Chizuru.database.authorize import add_auth, is_auth, rem_auth, is_auth, get_auth
from Chizuru import pbot as app, OWNER, TRIGGERS, LOGS


async def send_msg_or_document_text(text, message):
    if text:
        if len(text) > 4096:
            filename = 'output.txt'  
            with open(filename, "w+") as file:  
                file.write(text)    
            await message.reply_document(filename)
            os.remove(filename)
            return
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Message", url = message.link)]]))  
    else:
        try:
            await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Message", url = message.link)]]))
        except:
            await message.reply_text('Error',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Message", url = message.link)]]))        
                


async def get_users(id):
    try:
        get_users = await app.get_users(id)
        if get_users.username:
            USERNAME = get_users.username
        else:
            USERNAME = "None"
        if get_users.first_name:
            F_NAME = get_users.first_name
        else:
            F_NAME = "None"
        if get_users.last_name:
            L_NAME = get_users.last_name
        else:
              L_NAME = "None"
        if get_users.dc_id:
            DC_ID = get_users.dc_id
        else:
            DC_ID = "None"
        if get_users.status:
            STATUS = get_users.status
        else:
            STATUS = "None" 
        if get_users.photo.big_file_id:
            PBFI =  get_users.photo.big_file_id
        else:
            PBFI = "AQADBQADqrIxG_iZqFQAEAMAA2SnX3gABMVq60tkSk5LAAQeBA"      
    except:
        LOGS.info("Error No User Found")
        return  
    return USERNAME, F_NAME, L_NAME, DC_ID, STATUS,PBFI   

async def user_check_template(USERNAME, F_NAME, L_NAME, DC_ID, STATUS):
    TEXTS = f"**ᴜsᴇʀ's ғɪʀsᴛ ɴᴀᴍᴇ**: `{F_NAME}`\n" 
    TEXTS += f"**ᴜsᴇʀ's ʟᴀsᴛ sᴛᴀᴛᴜs**: `{L_NAME}`\n" 
    TEXTS += f"**ᴜsᴇʀ's ᴜsᴇʀɴᴀᴍᴇ**: @{USERNAME}\n"  
    TEXTS += f"**ᴜsᴇʀ's ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ**: `{DC_ID}`\n" 
    TEXTS += f"**ᴜsᴇʀ's ʟᴀsᴛ sᴛᴀᴛᴜs**: `{STATUS}`\n"        
    return TEXTS      
    