import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Chizuru.database.authorize import add_auth, is_auth, rem_auth, is_auth, get_auth
from Chizuru.utils.decorators import get_users, user_check_template
from Chizuru import pbot as app, OWNER, TRIGGERS, LOGS, UTRIGGERS

@app.on_message(filters.command(['auth', 'addsudo'], prefixes=TRIGGERS))
async def authorize(client:Client, msg:Message):
    
    check = is_auth(msg.from_user.id) 
    if check is False:
        await msg.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return 
    if msg.reply_to_message:
        reply = msg.reply_to_message
        user_id = reply.from_user.id
        add_auth(int(user_id))
        try:
            get_u = await get_users(user_id)
            pic_user = await client.download_media(get_u[5], file_name=f"user.png")
            TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4])
            try:
                await msg.reply_photo(pic_user, caption="`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))
            except:
                await msg.reply("`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))    
        except:
            LOGS.info('Error While Fetching User Info From Telegram Server')  
    user_id = msg.command[1]
    if user_id.isdigit():
        add_auth(int(user_id))
        try:
            get_u = await get_users(user_id)
            pic_user = await client.download_media(get_u[5], file_name=f"user.png")
            TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4])
            try:
                await msg.reply_photo(pic_user, caption="`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))
            except:
                await msg.reply("`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))    
        except:
            LOGS.info('Error While Adding User In Authorized List')  
    else:
        try:
            get_usersd = await client.get_users(msg.command[1])
        except BaseException:
            return await msg.reply("User Not Found")
        add_auth(int(get_usersd.id))
        get_u = await get_users(user_id)
        pic_user = await client.download_media(get_u[5], file_name=f"user.png")
        TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4])  
        try:
                await msg.reply_photo(pic_user, caption="`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))
        except:
            await msg.reply("`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))       

  
@app.on_message(filters.user(OWNER) & filters.command(['remauth', 'rmauth', 'deluser'], prefixes=TRIGGERS))
async def remove_authorize(client:Client, msg:Message):
    check = is_auth(msg.from_user.id) 
    if check is False:
        await msg.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    if msg.reply_to_message:
        reply = msg.reply_to_message
        user_id = reply.from_user.id
        rem_auth(int(user_id))
        try:
            get_u = await get_users(user_id)
            pic_user = await client.download_media(get_u[5], file_name=f"user.png")
            TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4])
            try:
                await msg.reply_photo(pic_user, caption="`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))
            except:
                await msg.reply("`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))    
        except:
            LOGS.info('Error While Fetching User Info From Telegram Server')  
    user_id = msg.command[1]
    if user_id.isdigit():
        rem_auth(int(user_id))
        try:
            get_u = await get_users(user_id)
            pic_user = await client.download_media(get_u[5], file_name=f"user.png")
            TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4])
            try:
                await msg.reply_photo(pic_user, caption="`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))
            except:
                await msg.reply("`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))    
        except:
            LOGS.info('Error While Removing User From Authorized List')  
    else:
        try:
            get_usersd = await client.get_users(msg.command[1])
        except BaseException:
            return await msg.reply("User Not Found")
        rem_auth(int(get_usersd.id))
        get_u = await get_users(user_id)
        pic_user = await client.download_media(get_u[5], file_name=f"user.png")
        TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4])  
        try:
                await msg.reply_photo(pic_user, caption="`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))
        except:
            await msg.reply("`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))       

                  
@app.on_message(filters.command('listauth', prefixes=TRIGGERS))
async def list_auth(client:Client, msg:Message): 
    check = is_auth(msg.from_user.id) 
    if check is False:
        await msg.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    users = get_auth()
    for id in users:
        try:
            o = await client.get_users(id)   
        except BaseException:
            o = None      
        if o:
            get_u = await get_users(o.id)
            pic_user = await client.download_media(get_u[5], file_name=f"user.png")
            TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4])
            try:
                await msg.reply_photo(pic_user, caption="`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))
            except:
                await msg.reply("`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ**`-------`\n\n"+ TEXTS, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("USER", url = f"https://t.me/{get_u[0]}")]]))   
        time.sleep(3)        
            
                     
            
            
              
          
        
        
