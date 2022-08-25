import os, random, time, sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Chizuru import pbot, TRIGGERS as trg, OWNER
from Chizuru.database.authorize import is_auth
from Chizuru.utils.progress import progress_for_pyrogram

@pbot.on_message(filters.document | filters.video | filters.photo | filters.command('rename', prefixes=trg))
async def download_(client: Client, message: Message):
    check = is_auth(message.from_user.id) 
    if check is False:
        await message.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]        
    dl = message.reply_to_message
    C_TIME = time.time()
    try:
        file_downloaded = await client.download_media(dl, progress=progress_for_pyrogram, progress_args=("**Downloading.....**",status_message, C_TIME))    
    except:
        status_message.edit('Error While Downloading File')    
    try:
        await message.reply_document(file_downloaded, thumb =f'downloads/thumb{message.from_user.id}.png', file_name=cmd, progress=progress_for_pyrogram, progress_args=("**Uploadding.....**",status_message, C_TIME))  
    except:
        await message.reply_document(file_downloaded, file_name=cmd, progress_args= ("**Uploadding.....**",status_message, C_TIME))  
    await status_message.delete()       
    os.remove(file_downloaded) 

@pbot.on_message(filters.command('sthumb', prefixes=trg))
async def set_thumb(client: Client, message: Message):
    check = is_auth(message.from_user.id) 
    if check is False:
        await message.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    if os.path.exists(f'downloads/thumb{message.from_user.id}.png') is True:
        os.remove(f'downloads/thumb{message.from_user.id}.png')
    status_message = await message.reply_text("Processing ...")       
    dl = message.reply_to_message
    if message.reply_to_message.photo:  
        ok = await pbot.download_media(dl, file_name=f'downloads/thumb{message.from_user.id}.png') 
        await status_message.delete()  
    else:
        await status_message.edit('Not Supported')      
        
@pbot.on_message(filters.command('vthumb', prefixes=trg))
async def view_thumb(client: Client, message: Message):
    check = is_auth(message.from_user.id) 
    if check is False:
        await message.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    if os.path.exists(f'downloads/thumb{message.from_user.id}.png') is True:
        await message.reply_photo(f'downloads/thumb{message.from_user.id}.png')  
    else:
        await message.reply('No Thumbnail Found') 
        
@pbot.on_message(filters.command('dthumb', prefixes=trg))
async def del_thumb(client: Client, message: Message):
    check = is_auth(message.from_user.id) 
    if check is False:
        await message.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    if os.path.exists(f'downloads/thumb{message.from_user.id}.png') is True:
        os.remove(f'downloads/thumb{message.from_user.id}.png')       

bot_version = os.environ.get('BOT_VERSION', 'HEROKU_CLR1.0')           


BUTTONS_DEV = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/sohailkhan_indianime'),
            InlineKeyboardButton('ɢɪᴛʜᴜʙ', url = 'https://github.com/soheru')
        ],
        [
            InlineKeyboardButton('ᴡᴇʙsɪᴛᴇ', url='https://teamyokai.tech'),
            InlineKeyboardButton('ᴄʜᴀɴɴᴇʟ', url='https://t.me/aboutmesk'),
        ],
        [
            InlineKeyboardButton('ɪɴsᴛᴀɢʀᴀᴍ', url='https://instagram.com/_soheru'),
            InlineKeyboardButton('ʜᴏᴍᴇ', 'help_go_home')
        ]
    ]
)

HOME = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", "help_about_dev"), 
            InlineKeyboardButton("ʜᴇʟᴘ", "help_about_dev"), 
        ]
    ]
)

HELP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ʟᴇᴇᴄʜ ғɪʟᴇ", "help_whatisleech"),
            InlineKeyboardButton("ᴛʜᴜᴍʙɴᴀɪʟ", "help_thumbnail"),
            InlineKeyboardButton("ʀᴇɴᴀᴍᴇ", "help_rename"),
            InlineKeyboardButton("ᴀᴜᴛʜᴏʀɪᴢᴇ", 'help_authandremove')
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", "help_about_dev")
        ]
    ]
)
 
@Client.on_callback_query(filters.regex('help'))
async def answer(client:Client, callback_query): 
    
    if 'whatisleech' in callback_query.data:
        await callback_query.message.edit("**How To Leech**\n\n👉**Leech with custom name** : `/download link | custom_name.mkv`\n👉**Leech normal**: `/download link`",reply_markup=HELP)
    elif 'rename' in callback_query.data: 
        await callback_query.message.edit("**Rename Files**\n\n👉`/rename new_name.mkv`",reply_markup=HELP)
    elif 'thumbnail' in callback_query.data:
        await callback_query.message.edit("**Thumbnail**\n\n👉**Set Thumbnail** : `/sthumb` message reply to photo\n👉**Remove Thumbnail** : `/dthumb` remove delete\n👉**View Thumbnail** : `/vthumb` to check current thumbnail",reply_markup=HELP)
    elif 'go_home' in callback_query.data:
        text = f"**Konnichiwa**, `{callback_query.message.from_user.first_name}`\n\nI'm Chizuru An Leech And File Renaming Bot Made By [Soheru San](https://t.me/sohailkhan_indianime)\n\n**My Version** - `{bot_version}`\n**Heroku Supported** - `True`\n**Pyrogram Version** - `1.16.4`"
        await callback_query.message.edit(text, reply_markup = HOME)
    elif 'about_dev' in callback_query.data:
        text = f'Hello `{callback_query.from_user.first_name}`,\n\n'
        text += "I'm Sohail\nTo connect with me, Check Below Buttons"
        await callback_query.message.edit(text, reply_markup=BUTTONS_DEV)             
    elif 'helpsd' in callback_query.data:
        await callback_query.message.edit(f'**Hello `{Client.get_users(callback_query.from_user.id).mention()}`**,\n\nUse Below Buttons To Check Our Modules.', reply_markup=HELP)  
    elif 'authandremove' in callback_query.data:
        text = "**Add Sudo**\n`/auth` message reply user\n`/auth userid`\n`/auth usernam`\n\n"
        text += "**Remove Sudo**\n`/remauth` message reply user\n`/remauth userid`\n`/remauth usernam`\n\n"
        text += "**List Auth Users** : `/listauth`"
    await callback_query.answer("Done")     
@pbot.on_message(filters.command('start', prefixes=trg))
async def start_bot_text(client: Client, message: Message):
    images = os.listdir('./Images/Start')
    texts = f"**Konnichiwa**, `{message.from_user.first_name}`\n\nI'm Chizuru An Leech And File Renaming Bot Made By [Soheru San](https://t.me/sohailkhan_indianime)\n\n**My Version** - `{bot_version}`\n**Heroku Supported** - `True`\n**Pyrogram Version** - `1.16.4`"
    await message.reply_photo(f'./Images/Start/{random.choice(images)}', caption=texts, reply_markup=HOME)

    
@pbot.on_message(filters.command('restart', prefixes=trg))
async def restart_bot(client: pbot, message: Message):  
    check = is_auth(message.from_user.id) 
    if check is False:
        await message.reply("You Are Not Authorized To Perform This Action Contact Admins")
        return
    msg = await message.reply("Restarting", reply_markup=HOME)
    os.execl(sys.executable, sys.executable, "-m", "Bot")      
                   
