import re
import sys
import os
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID=63460
API_HASH="76ce72c3c4cb49fd6d456bd07dce3435"
BOT_TOKEN= os.getenv("BOT_TOKEN", "6956883087:AAGflukIkI-y89usGn5fNYZcKmKf54mAaJM")
OWNER_USERNAME= os.getenv("OWNER_USERNAME", "owner_username")
OWNER_ID= os.getenv("OWNER_ID", 544633527)
WELCOME_MSG = os.getenv("WELCOME_MSG", "Welcome to the group! I'm here to assist you.")
CUSTOM_MSG = os.getenv("CUSTOM_MSG", "Lets get started!\nI am #1 bot in the world\nI can serve you unlimited entertainment\n")
BUTTON_TYPE = "grid"
BUTTON_MODE = "inline"
