#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ربات تلگرام ساده و کاربردی
"""

import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیمات ربات
try:
    # اول از متغیرهای محیطی
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID')
    
    # اگر نبود، از config.py
    if not BOT_TOKEN or not OWNER_CHAT_ID:
        from config import BOT_TOKEN as CONFIG_BOT_TOKEN, OWNER_CHAT_ID as CONFIG_OWNER_CHAT_ID
        from config import WELCOME_MESSAGE, FORWARD_MESSAGE_PREFIX
        
        if not BOT_TOKEN:
            BOT_TOKEN = CONFIG_BOT_TOKEN
        if not OWNER_CHAT_ID:
            OWNER_CHAT_ID = CONFIG_OWNER_CHAT_ID
    else:
        # پیام‌های پیش‌فرض
        WELCOME_MESSAGE = """
به ربات پشتیبانی FreeNetBox خوش آمدید! 🌟

ما آماده کمک به شما هستیم.
"""
        FORWARD_MESSAGE_PREFIX = "📩 پیام جدید از کاربر:\n\n"
        
        # سعی کن از config.py بخونی
        try:
            from config import WELCOME_MESSAGE as CONFIG_WELCOME, FORWARD_MESSAGE_PREFIX as CONFIG_PREFIX
            WELCOME_MESSAGE = CONFIG_WELCOME
            FORWARD_MESSAGE_PREFIX = CONFIG_PREFIX
        except:
            pass
            
except ImportError:
    # fallback به متغیرهای محیطی
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID', 'YOUR_CHAT_ID_HERE')
    WELCOME_MESSAGE = """
به ربات پشتیبانی FreeNetBox خوش آمدید! 🌟

ما آماده کمک به شما هستیم.
"""
    FORWARD_MESSAGE_PREFIX = "📩 پیام جدید از کاربر:\n\n"

# تنظیم لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        """راه‌اندازی ربات"""
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def get_main_menu(self):
        """ایجاد منوی اصلی"""
        keyboard = [
            [KeyboardButton("📱 چه برنامه ای نیاز دارم")],
            [KeyboardButton("🔗 لینک برنامه ها")],
            [KeyboardButton("💰 لیست قیمت اکانت")],
            [KeyboardButton("📢 لینک کانال و پشتیبانی سریع")],
            [KeyboardButton("📚 راهنمای کامل برنامه")],
            [KeyboardButton("❌ انصراف")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def get_start_menu(self):
        """منوی شروع برای انصراف"""
        keyboard = [
            [KeyboardButton("🚀 شروع")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def setup_handlers(self):
        """تنظیم هندلرهای ربات"""
        # دستورات اصلی
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        
        # گزینه‌های منو
        self.application.add_handler(MessageHandler(filters.Regex("📱 چه برنامه ای نیاز دارم"), self.handle_apps_needed))
        self.application.add_handler(MessageHandler(filters.Regex("🔗 لینک برنامه ها"), self.handle_app_links))
        self.application.add_handler(MessageHandler(filters.Regex("💰 لیست قیمت اکانت"), self.handle_price_list))
        self.application.add_handler(MessageHandler(filters.Regex("📢 لینک کانال و پشتیبانی سریع"), self.handle_support_links))
        self.application.add_handler(MessageHandler(filters.Regex("📚 راهنمای کامل برنامه"), self.handle_complete_guide))
        self.application.add_handler(MessageHandler(filters.Regex("❌ انصراف"), self.handle_cancel))
        
        # دکمه شروع
        self.application.add_handler(MessageHandler(filters.Regex("🚀 شروع"), self.start_command))
        
        # پیام‌های عمومی
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پاسخ به دستور /start"""
        user = update.effective_user
        welcome_text = f"سلام {user.first_name}! 👋\n\n{WELCOME_MESSAGE}\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
        
        await update.message.reply_text(welcome_text, reply_markup=self.get_main_menu())
        
        # اطلاع به مالک
        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"🔔 کاربر جدید:\n👤 {user.first_name}\n🆔 {user.id}"
            )
        except:
            pass

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """راهنما"""
        help_text = """🤖 راهنمای ربات:

دستورات:
/start - شروع
/menu - منو
/help - راهنما

گزینه‌ها:
📱 چه برنامه ای نیاز دارم
🔗 لینک برنامه ها
💰 لیست قیمت اکانت
📢 لینک کانال و پشتیبانی سریع
📚 راهنمای کامل برنامه
❌ انصراف"""
        
        await update.message.reply_text(help_text, reply_markup=self.get_main_menu())

    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش منو"""
        await update.message.reply_text("لطفاً گزینه مورد نظر را انتخاب کنید:", reply_markup=self.get_main_menu())

    async def handle_apps_needed(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """راهنمای برنامه‌های مورد نیاز"""
        user = update.effective_user
        
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
        
        await update.message.reply_text(apps_info, reply_markup=self.get_main_menu())
        
        # اطلاع به مالک
        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"📱 درخواست لیست برنامه‌ها از {user.first_name} ({user.id})"
            )
        except:
            pass

    async def handle_app_links(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """لینک برنامه‌ها"""
        user = update.effective_user
        
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
        
        await update.message.reply_text(links_info, reply_markup=self.get_main_menu())
        
        # اطلاع به مالک
        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"🔗 درخواست لینک برنامه‌ها از {user.first_name} ({user.id})"
            )
        except:
            pass

    async def handle_price_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """لیست قیمت اکانت"""
        user = update.effective_user
        
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
        
        await update.message.reply_text(price_info, reply_markup=self.get_main_menu())
        
        # اطلاع به مالک
        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"💰 درخواست لیست قیمت از {user.first_name} ({user.id})"
            )
        except:
            pass

    async def handle_support_links(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """لینک کانال و پشتیبانی"""
        user = update.effective_user
        
        support_info = """📢 لینک کانال و پشتیبانی سریع:

👨‍💻 پشتیبانی: @freeNetBoxSupport
📢 کانال: @FreeNet2Box

💡 برای سوالات و خرید اکانت به پشتیبانی مراجعه کنید."""
        
        await update.message.reply_text(support_info, reply_markup=self.get_main_menu())
        
        # اطلاع به مالک
        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"📢 درخواست لینک‌های پشتیبانی از {user.first_name} ({user.id})"
            )
        except:
            pass

    async def handle_complete_guide(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """راهنمای کامل برنامه (فعلاً خالی)"""
        user = update.effective_user
        
        guide_info = """📚 راهنمای کامل برنامه:

🚧 این بخش در حال تکمیل است...

⏳ به زودی راهنمای کاملی از نحوه استفاده از برنامه‌ها در اختیارتان قرار خواهیم داد.

💬 برای اطلاعات بیشتر با پشتیبانی تماس بگیرید: @freeNetBoxSupport"""
        
        await update.message.reply_text(guide_info, reply_markup=self.get_main_menu())
        
        # اطلاع به مالک
        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"📚 درخواست راهنمای کامل از {user.first_name} ({user.id})"
            )
        except:
            pass

    async def handle_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """انصراف"""
        cancel_text = """❌ عملیات لغو شد.

🏠 برای شروع مجدد ربات، دکمه زیر را فشار دهید:"""
        
        await update.message.reply_text(cancel_text, reply_markup=self.get_start_menu())

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پیام‌های آزاد"""
        user = update.effective_user
        message = update.message
        
        response = """پیام شما دریافت شد! 📩

از منوی زیر گزینه مورد نظر را انتخاب کنید:"""
        
        await message.reply_text(response, reply_markup=self.get_main_menu())
        
        # ارسال به مالک
        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"💬 پیام آزاد از {user.first_name} ({user.id}):\n{message.text}"
            )
        except:
            pass

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عکس"""
        user = update.effective_user
        await update.message.reply_text("عکس دریافت شد! 📸", reply_markup=self.get_main_menu())
        
        try:
            await context.bot.send_photo(
                chat_id=OWNER_CHAT_ID,
                photo=update.message.photo[-1].file_id,
                caption=f"📸 عکس از {user.first_name} ({user.id})"
            )
        except:
            pass

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """صدا"""
        user = update.effective_user
        await update.message.reply_text("پیام صوتی دریافت شد! 🎤", reply_markup=self.get_main_menu())
        
        try:
            await context.bot.send_voice(
                chat_id=OWNER_CHAT_ID,
                voice=update.message.voice.file_id,
                caption=f"🎤 صدا از {user.first_name} ({user.id})"
            )
        except:
            pass

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """فایل"""
        user = update.effective_user
        await update.message.reply_text("فایل دریافت شد! 📎", reply_markup=self.get_main_menu())
        
        try:
            await context.bot.send_document(
                chat_id=OWNER_CHAT_ID,
                document=update.message.document.file_id,
                caption=f"📎 فایل از {user.first_name} ({user.id})"
            )
        except:
            pass

    def run(self):
        """اجرای ربات با error handling بهتر"""
        try:
            logger.info("🤖 ربات تلگرام شروع شد...")
            logger.info("🔄 در انتظار پیام‌ها...")
            
            # اجرای ساده و سازگار با نسخه 20.8
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES
            )
        except Exception as e:
            logger.error(f"❌ خطا در اجرای ربات: {e}")
            raise

def main():
    """تابع اصلی"""
    try:
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ لطفاً توکن ربات را تنظیم کنید")
            raise ValueError("BOT_TOKEN not configured")
        
        if OWNER_CHAT_ID == "YOUR_CHAT_ID_HERE":
            logger.error("❌ لطفاً Chat ID را تنظیم کنید")
            raise ValueError("OWNER_CHAT_ID not configured")
        
        bot = TelegramBot()
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("⏹️ ربات توسط کاربر متوقف شد.")
    except Exception as e:
        logger.error(f"❌ خطا در main: {e}")
        raise

if __name__ == "__main__":
    main() 