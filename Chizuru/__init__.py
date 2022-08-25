import os
import logging
import time
import sys
from pyrogram import Client

logging.basicConfig(level=logging.INFO)

LOGS = logging.getLogger("AnimeBot")
LOGS.setLevel(level=logging.INFO)

#-------------------------------LIST----------------------------------------

#-------------------------------VARS-----------------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN",None)
API_ID = int(os.environ.get("API_ID",None))
API_HASH = os.environ.get("API_HASH",None)
MONGO_DB = os.environ.get("MONGO_DB", None)
OWNER = int(os.environ.get("OWNER",953362604))
#-------------------------------DEFAULT---------------------------------------
TRIGGERS = os.environ.get("TRIGGERS", "/").split()
UTRIGGERS = os.environ.get("TRIGGERS", ".").split()
plugins = dict(root="Chizuru/plugin")
#------------------------------CONNECTION------------------------------------
if BOT_TOKEN is not None:
    try:
        pbot = Client("Chizuru", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=plugins)
        LOGS.info("❤️ Bot Connected")
    except:
        LOGS.info('😞 Error While Connecting To Bot')    
        sys.exit()            
