#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ربات تلگرام ساده - سازگار با نسخه 20.8+
"""

import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیم لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تنظیمات
BOT_TOKEN = os.getenv('BOT_TOKEN', '7839007712:AAERxGdintfRM6xMAwoTWVtOipzRPvyf3Gs')
OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID', '5643687492')

def get_main_menu():
    """منوی اصلی"""
    keyboard = [
        ["📱 چه برنامه ای نیاز دارم"],
        ["🔗 لینک برنامه ها"],
        ["💰 لیست قیمت اکانت"],
        ["📢 لینک کانال و پشتیبانی سریع"],
        ["📚 راهنمای کامل برنامه"],
        ["❌ انصراف"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_start_menu():
    """منوی شروع"""
    keyboard = [["🚀 شروع"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user = update.effective_user
    welcome_text = f"""سلام {user.first_name}! 👋

به ربات پشتیبانی FreeNetBox خوش آمدید! 🌟

ما آماده کمک به شما هستیم.

لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"""
    
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu())
    
    # اطلاع به مالک
    try:
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"🔔 کاربر جدید:\n👤 {user.first_name}\n🆔 {user.id}"
        )
    except:
        pass

async def handle_apps_needed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنمای برنامه‌ها"""
    apps_info = """📱 برنامه‌های مورد نیاز:

🍎 iOS:
• Streisand | V2BOX

🤖 Android:
• V2rayNG | V2BOX | NekoBox

🖥️ Windows:
• V2rayN | Nekoray

🍎 macOS:
• Streisand | V2BOX

🐧 Linux:
• V2rayN

💡 توصیه: از جدیدترین نسخه برنامه‌ها استفاده کنید."""
    
    await update.message.reply_text(apps_info, reply_markup=get_main_menu())

async def handle_app_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لینک برنامه‌ها"""
    links_info = """🔗 لینک برنامه‌ها:

🍎 iOS:
• Streisand: https://apps.apple.com/us/app/streisand/id6450534064
• V2BOX: https://apps.apple.com/us/app/v2box-v2ray-client/id6446814690

🤖 Android:
• V2rayNG: https://github.com/2dust/v2rayNG/releases/download/1.8.38/v2rayNG_1.8.38_universal.apk
• V2BOX: https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box&hl=en

🍎 macOS:
• Streisand: https://apps.apple.com/us/app/streisand/id6450534064
• V2BOX: https://apps.apple.com/us/app/v2box-v2ray-client/id6446814690

🐧 Linux:
• V2rayN: https://github.com/2dust/v2rayN/releases/download/7.12.7/v2rayN-linux-64.zip"""
    
    await update.message.reply_text(links_info, reply_markup=get_main_menu())

async def handle_price_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست قیمت"""
    price_info = """💰 لیست قیمت اکانت:

🔹 فعال سازی:

🔘 اکانت های ۱ ماهه:
-> ۲۵ گیگ: ۱۸۰ تومان
-> ۵۰ گیگ: ۲۵۰ تومان  
-> ۱۰۰ گیگ: ۳۸۰ تومان

🔘 اکانت های ۳ ماهه:
-> ۱۵۰ گیگ: ۶۸۰ تومان
-> ۲۰۰ گیگ: ۷۹۰ تومان

💬 برای خرید با پشتیبانی تماس بگیرید"""
    
    await update.message.reply_text(price_info, reply_markup=get_main_menu())

async def handle_support_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لینک پشتیبانی"""
    support_info = """📢 لینک کانال و پشتیبانی سریع:

👨‍💻 پشتیبانی: @freeNetBoxSupport
📢 کانال: @FreeNet2Box

💡 برای سوالات و خرید اکانت به پشتیبانی مراجعه کنید."""
    
    await update.message.reply_text(support_info, reply_markup=get_main_menu())

async def handle_complete_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنمای کامل"""
    guide_info = """📚 راهنمای کامل برنامه:

🚧 این بخش در حال تکمیل است...

⏳ به زودی راهنمای کاملی از نحوه استفاده از برنامه‌ها در اختیارتان قرار خواهیم داد.

💬 برای اطلاعات بیشتر با پشتیبانی تماس بگیرید: @freeNetBoxSupport"""
    
    await update.message.reply_text(guide_info, reply_markup=get_main_menu())

async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """انصراف"""
    cancel_text = """❌ عملیات لغو شد.

🏠 برای شروع مجدد ربات، دکمه زیر را فشار دهید:"""
    
    await update.message.reply_text(cancel_text, reply_markup=get_start_menu())

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دکمه شروع"""
    await start_command(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام‌های عمومی"""
    user = update.effective_user
    message = update.message
    
    response = """پیام شما دریافت شد! 📩

از منوی زیر گزینه مورد نظر را انتخاب کنید:"""
    
    await message.reply_text(response, reply_markup=get_main_menu())
    
    # ارسال به مالک
    try:
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"💬 پیام از {user.first_name} ({user.id}):\n{message.text}"
        )
    except:
        pass

def main():
    """تابع اصلی"""
    logger.info("🤖 شروع ربات تلگرام ساده...")
    
    # ساخت Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.Regex("📱 چه برنامه ای نیاز دارم"), handle_apps_needed))
    application.add_handler(MessageHandler(filters.Regex("🔗 لینک برنامه ها"), handle_app_links))
    application.add_handler(MessageHandler(filters.Regex("💰 لیست قیمت اکانت"), handle_price_list))
    application.add_handler(MessageHandler(filters.Regex("📢 لینک کانال و پشتیبانی سریع"), handle_support_links))
    application.add_handler(MessageHandler(filters.Regex("📚 راهنمای کامل برنامه"), handle_complete_guide))
    application.add_handler(MessageHandler(filters.Regex("❌ انصراف"), handle_cancel))
    application.add_handler(MessageHandler(filters.Regex("🚀 شروع"), handle_start_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🔄 در انتظار پیام‌ها...")
    
    # اجرای ربات
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 