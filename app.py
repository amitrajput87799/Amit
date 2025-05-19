import os
import logging
import yaml
import re
from datetime import datetime
from time import sleep
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
import sys
try:
    from config import API_ID, API_HASH, BOT_TOKEN, WELCOME_MSG, BUTTON_TYPE, BUTTON_MODE, CUSTOM_MSG, OWNER_ID
except ImportError:
    print("Error: config.py missing required variables.")
    print("Please ensure API_ID, API_HASH, BOT_TOKEN are defined in config.py")
    exit()

try:
    with open("msg.yml", 'r', encoding='utf-8') as f:
        messages = yaml.safe_load(f)
    MENU_MSG = messages['menu']
    BUY_MSG = messages['buy'] 
    PAYMENT_MSG = messages['payMethod']
except FileNotFoundError:
    print("Error: msg.yml not found.")
    exit()
except KeyError as e:
    print(f"Error: Missing key {e} in msg.yml. Ensure 'menu', 'buy', and 'payMethod' are defined.")
    exit()


logging.basicConfig(
    level=logging.ERROR,  ## Change to logging.DEBUG for more verbosity
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set in config.py or .env file.\nExiting.")
    exit()
    
app = Client(
    "xbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def create_inline_keyboard():
    menu_button = InlineKeyboardButton("MENU 🛍️", callback_data="menu_callback")
    buy_now_button = InlineKeyboardButton("BUY NOW 💰", callback_data="buy_now_callback")
    payment_methods_button = InlineKeyboardButton("PAYMENT METHODS 💳", callback_data="payment_methods_callback")

    if BUTTON_TYPE == "grid":
        keyboard = [[menu_button, buy_now_button, payment_methods_button]]
    else: 
        keyboard = [
            [menu_button],
            [buy_now_button],
            [payment_methods_button]
        ]
    return InlineKeyboardMarkup(keyboard)

def create_chat_keyboard():
    menu_button = KeyboardButton("MENU 🛍️")
    buy_now_button = KeyboardButton("BUY NOW 💰")
    payment_methods_button = KeyboardButton("PAYMENT METHODS 💳")
    if BUTTON_TYPE == "grid":
        keyboard = [[menu_button, buy_now_button, payment_methods_button]]
    else:
        keyboard = [
            [menu_button],
            [buy_now_button],
            [payment_methods_button]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

@app.on_message((filters.command("menu") | filters.regex("^MENU 🛍️$")) & filters.private)
async def menu_command(client, message):
    try:
        await message.reply_text(MENU_MSG)
    except Exception as e:
        logger.error(f"Error in menu_command: {e}")

@app.on_message((filters.command("payments") | filters.regex("^PAYMENT METHODS 💳$")) & filters.private)
async def payments_command(client, message):
    try:
        await message.reply_text(PAYMENT_MSG)
    except Exception as e:
        logger.error(f"Error in payments_command: {e}")

@app.on_message((filters.command(["contact", "support", "settings" "help"]) | filters.regex("^BUY NOW 💰")) & filters.private)

async def contact_command(client, message):
    try:
        await message.reply_text(BUY_MSG)
    except Exception as e:
        logger.error(f"Error in contact_command: {e}")

@app.on_message((filters.command("id") | filters.regex("^me")) & filters.private)
async def id_command(client, message):
    try:
        user = message.from_user
        user_info = f"""
👤 **USER INFORMATION**
• **ID**: `{user.id}`
• **First Name**: {user.first_name}
• **Last Name**: {user.last_name or 'Not set'}
• **Username**: {'@' + user.username if user.username else 'Not set'}
• **Language Code**: {user.language_code or 'Unknown'}
• **DC ID**: {getattr(user, "dc_id", 'Unknown')}
• **Phone Number**: {getattr(user, "phone_number", 'Unknown')}
• **Premium ** {'Yes' if user.is_premium else 'No'} | **Verified**: {'Yes' if user.is_verified else 'No'}

        """
        await message.reply_text(user_info)
    except Exception as e:
        logger.error(f"Error in id_command: {e}")


@app.on_callback_query(filters.regex("^menu_callback$"))
async def menu_callback_handler(client, callback_query):
    try:
        await menu_command(client, callback_query.message)
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Error in menu_callback_handler: {e}")
        await callback_query.answer("An error occurred.", show_alert=True)

@app.on_callback_query(filters.regex("^buy_now_callback$"))
async def buy_now_callback_handler(client, callback_query):
    try:
        await contact_command(client, callback_query.message)
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Error in buy_now_callback_handler: {e}")
        await callback_query.answer("An error occurred.", show_alert=True)

@app.on_callback_query(filters.regex("^payment_methods_callback$"))
async def payment_methods_callback_handler(client, callback_query):
    try:
        await payments_command(client, callback_query.message)
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Error in payment_methods_callback_handler: {e}")
        await callback_query.answer("An error occurred.", show_alert=True)


@app.on_message(filters.command("menu") & filters.private)
async def chat_keyboard_handler(client, message):
    if BUTTON_MODE != "chat":
        return
    text = message.text.strip().lower()
    if text.startswith("menu"):   
        await message.reply_text(MENU_MSG) 

@app.on_message(filters.command("admin") & filters.private)
async def admin_command(client, message):
    if not OWNER_ID:
        await message.reply_text("This feature is disabled.")
        return

    if message.from_user.id != int(OWNER_ID):
        await message.reply_text("You are not authorized to use this command.")
        return
    admin_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("BUTTON TYPE - How buttons are shown!", callback_data="admin_button_type")],
        [InlineKeyboardButton("BUTTON MODE - Where to show button!", callback_data="admin_button_mode")],
        [InlineKeyboardButton("Exit", callback_data="admin_exit")]
    ])

    await message.reply_text(f"Hi, Owner! I am up and working.\nYou can use `reboot` to reboot/restart the bot anytime..", reply_markup=admin_menu)

@app.on_callback_query(filters.regex("^admin_button_type$"))
async def admin_button_type(client, callback_query: CallbackQuery):
    button_type_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Grid {'✅' if BUTTON_TYPE == 'grid' else ''}", callback_data="set_button_type_grid")],
        [InlineKeyboardButton(f"List {'✅' if BUTTON_TYPE == 'list' else ''}", callback_data="set_button_type_list")],
        [InlineKeyboardButton("Back", callback_data="admin_exit")]
    ])

    await callback_query.message.edit_text("Select how button will appear!\nGride: All button in 1 line\nList: One button per line.", reply_markup=button_type_menu)

@app.on_callback_query(filters.regex("^admin_button_mode$"))
async def admin_button_mode(client, callback_query: CallbackQuery):
    button_mode_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Inline {'✅' if BUTTON_MODE == 'inline' else ''}", callback_data="set_button_mode_inline")],
        [InlineKeyboardButton(f"Chat {'✅' if BUTTON_MODE == 'chat' else ''}", callback_data="set_button_mode_chat")],
        [InlineKeyboardButton("EXIT", callback_data="admin_exit")]
    ])

    await callback_query.message.edit_text("Where shall button be shown!\nChat: Inside chat\nInline: As menu below the bot (not inside the chat)", reply_markup=button_mode_menu)

@app.on_callback_query(filters.regex("^set_button_type_(grid|list)$"))
async def set_button_type(client, callback_query: CallbackQuery):
    global BUTTON_TYPE
    BUTTON_TYPE = callback_query.data.split("_")[-1]
    update_config("BUTTON_TYPE", BUTTON_TYPE)
    await callback_query.answer("BUTTON TYPE updated.")
    await callback_query.message.edit_text("Bot restarted & updated button type...")
    restart_bot(callback_query.message)

@app.on_callback_query(filters.regex("^set_button_mode_(inline|chat)$"))
async def set_button_mode(client, callback_query: CallbackQuery):
    global BUTTON_MODE
    BUTTON_MODE = callback_query.data.split("_")[-1]
    update_config("BUTTON_MODE", BUTTON_MODE)
    await callback_query.answer("BUTTON MODE updated.")
    await callback_query.message.edit_text("Bot restarted and updated button mode...")
    restart_bot(callback_query.message)

@app.on_callback_query(filters.regex("^admin_exit$"))
async def admin_exit(client, callback_query: CallbackQuery):
    await callback_query.message.delete()

def update_config(key, value):
    config_path = "config.py"
    with open(config_path, "r") as file:
        lines = file.readlines()

    with open(config_path, "w") as file:
        for line in lines:
            if line.startswith(f"{key} ="):
                file.write(f"{key} = \"{value}\"\n")
            else:
                file.write(line)



@app.on_message((filters.command("start") | filters.regex("^start")) & filters.private)
#@app.on_message(filters.command("start") & filters.private)
async def start_message(client, message):

    try:
        if BUTTON_MODE == "chat":
            await message.reply_text(
                WELCOME_MSG,
                reply_markup=create_inline_keyboard()
            )
        else:
            await message.reply_text(WELCOME_MSG)
            import asyncio
            await asyncio.sleep(2)
            await message.reply(CUSTOM_MSG,
                reply_markup=create_chat_keyboard()
            )
    except Exception as e:
        logger.error(f"Error in start_command: {e}")


def notify_owner_on_start():
    try:
        if OWNER_ID:
            currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.send_message(
                chat_id=OWNER_ID,
                text=(f"Booting up\nNow {currentTime}")
            )
    except Exception as e:
        #Pass do not throw error/
        pass
        
@app.on_message((filters.command("reboot") | filters.regex("^re")) & filters.private)
async def reboot_command(client, message):
    if message.from_user.id != int(OWNER_ID):
        await message.reply_text("You are not authorized to use this command.")
        return
    try:
        await message.reply_text("Restarting bot...")
        sleep(2)
        restart_bot(message)
    except Exception as e:
        await message.reply_text("Failed to restart the bot.")
        pass
    finally:
        logger.info("Bot restarted...")

def restart_bot(message):
    os.execv(sys.executable, [sys.executable] + sys.argv)


if __name__ == "__main__":
    try:
        
        app.start() 
        notify_owner_on_start() 
        idle()  
        print ("Bot started successfully.") 
    except Exception as e:
        logger.error(f"WHAT WENT WRONG?: {e}")
    finally:
        logger.info("Bot stopped.")
