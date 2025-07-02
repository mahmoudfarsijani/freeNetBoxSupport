#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ربات تلگرام برای دریافت پیام‌ها و ارسال پاسخ خودکار
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from config import BOT_TOKEN, OWNER_CHAT_ID, WELCOME_MESSAGE, FORWARD_MESSAGE_PREFIX

# تنظیم لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تعریف منوهای ربات
def get_main_menu():
    """ایجاد منوی اصلی"""
    keyboard = [
        [KeyboardButton("🔴 قطع هستم لطفا سریع بررسی کن")],
        [KeyboardButton("🔄 میخوام اکانتمو تمدید کن")],
        [KeyboardButton("📢 لینک چنل رو بهم بده")],
        [KeyboardButton("💰 میخوام اکانت بخرم")],
        [KeyboardButton("❌ انصراف")]
    ]
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        one_time_keyboard=False
    )

def get_account_plans():
    """لیست پلان‌های اکانت"""
    return """👁 تو محدودترین روزا پرسرعت کنار شماییم

🔹 فعال سازی:

🔘 اکانت های ۱ ماهه:
-> ۲۵ گیگ: ۱۸۰ تومان
-> ۵۰ گیگ: ۲۵۰ تومان  
-> ۱۰۰ گیگ: ۳۸۰ تومان

🔘 اکانت های ۳ ماهه:
-> ۱۵۰ گیگ: ۶۸۰ تومان
-> ۲۰۰ گیگ: ۷۹۰ تومان

💬 پشتیبانی: @freeNetBoxSupport"""

class TelegramBot:
    def __init__(self):
        """راه‌اندازی ربات"""
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """تنظیم هندلرهای ربات"""
        # هندلر برای دستور /start
        self.application.add_handler(CommandHandler("start", self.start_command))
        
        # هندلر برای دستور /help
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # هندلر برای دستور /menu
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        
        # هندلر برای دستور /reset (در صورت گیج شدن کاربر)
        self.application.add_handler(CommandHandler("reset", self.reset_command))
        
        # هندلرهای منو
        self.application.add_handler(MessageHandler(filters.Regex("🔴 قطع هستم لطفا سریع بررسی کن"), self.handle_connection_issue))
        self.application.add_handler(MessageHandler(filters.Regex("🔄 میخوام اکانتمو تمدید کن"), self.handle_renewal))
        self.application.add_handler(MessageHandler(filters.Regex("📢 لینک چنل رو بهم بده"), self.handle_channel_link))
        self.application.add_handler(MessageHandler(filters.Regex("💰 میخوام اکانت بخرم"), self.handle_buy_account))
        self.application.add_handler(MessageHandler(filters.Regex("❌ انصراف"), self.handle_cancel))
        
        # هندلر برای تمام پیام‌های متنی (در آخر قرار دهید)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # هندلر برای عکس‌ها
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        
        # هندلر برای صداها
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        
        # هندلر برای فایل‌ها
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پاسخ به دستور /start"""
        try:
            user = update.effective_user
            welcome_text = f"سلام {user.first_name}! 👋\n\n{WELCOME_MESSAGE}\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
            
            await update.message.reply_text(
                welcome_text,
                reply_markup=get_main_menu()
            )
            
            # اطلاع به مالک ربات
            try:
                await context.bot.send_message(
                    chat_id=OWNER_CHAT_ID,
                    text=f"🔔 کاربر جدید ربات را شروع کرد:\n"
                         f"نام: {user.first_name} {user.last_name or ''}\n"
                         f"نام کاربری: @{user.username or 'ندارد'}\n"
                         f"شناسه: {user.id}"
                )
            except Exception as e:
                logger.error(f"خطا در ارسال اطلاع به مالک: {e}")
                
        except Exception as e:
            logger.error(f"خطا در start_command: {e}")
            try:
                await update.message.reply_text("سلام! ربات آماده است:", reply_markup=get_main_menu())
            except Exception as inner_e:
                logger.error(f"خطا در پیام پشتیبان start: {inner_e}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پاسخ به دستور /help"""
        try:
            help_text = """
🤖 راهنمای استفاده از ربات:

• از منوی زیر گزینه مورد نظر را انتخاب کنید
• برای نمایش مجدد منو از /menu استفاده کنید
• برای ریست کردن ربات از /reset استفاده کنید
• برای شروع از دستور /start استفاده کنید

گزینه‌های موجود:
🔴 بررسی قطعی اینترنت
🔄 تمدید اکانت
📢 لینک کانال
💰 خرید اکانت جدید
❌ انصراف (بازگشت به منو)

دستورات مفید:
/start - شروع مجدد
/menu - نمایش منو
/reset - ریست ربات
/help - نمایش این راهنما
            """
            await update.message.reply_text(help_text, reply_markup=get_main_menu())
        except Exception as e:
            logger.error(f"خطا در help_command: {e}")

    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش منوی اصلی"""
        try:
            await update.message.reply_text(
                "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
                reply_markup=get_main_menu()
            )
        except Exception as e:
            logger.error(f"خطا در نمایش منو: {e}")

    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ریست کردن ربات و نمایش منوی اصلی"""
        try:
            user = update.effective_user
            reset_text = """🔄 ربات ریست شد!
            
🏠 به منوی اصلی بازگشتید.
از گزینه‌های زیر انتخاب کنید:"""
            
            await update.message.reply_text(
                reset_text,
                reply_markup=get_main_menu()
            )
            
            logger.info(f"کاربر {user.first_name} ({user.id}) ربات را ریست کرد")
            
        except Exception as e:
            logger.error(f"خطا در reset_command: {e}")
            try:
                await update.message.reply_text(
                    "🔄 ربات آماده است:",
                    reply_markup=get_main_menu()
                )
            except Exception as inner_e:
                logger.error(f"خطا در ارسال پیام پشتیبان ریست: {inner_e}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش پیام‌های متنی آزاد"""
        user = update.effective_user
        message = update.message
        
        # ارسال پاسخ خودکار به کاربر همراه با منو
        response_text = f"""پیام شما دریافت شد! 📩

لطفاً از منوی زیر گزینه مورد نظر خود را انتخاب کنید:"""
        
        await message.reply_text(response_text, reply_markup=get_main_menu())
        
        # ارسال پیام به مالک ربات
        forward_text = (
            f"{FORWARD_MESSAGE_PREFIX}"
            f"👤 از: {user.first_name} {user.last_name or ''}\n"
            f"📱 نام کاربری: @{user.username or 'ندارد'}\n"
            f"🆔 شناسه: {user.id}\n"
            f"📅 تاریخ: {message.date}\n"
            f"{'='*30}\n"
            f"💬 پیام آزاد:\n{message.text}"
        )
        
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=forward_text
        )
        
        logger.info(f"پیام آزاد از {user.first_name} ({user.id}) دریافت و ارسال شد")

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش عکس‌ها"""
        user = update.effective_user
        message = update.message
        
        # ارسال پاسخ خودکار
        await message.reply_text(WELCOME_MESSAGE)
        
        # ارسال عکس به مالک
        caption = (
            f"📸 عکس جدید از:\n"
            f"👤 {user.first_name} {user.last_name or ''}\n"
            f"📱 @{user.username or 'ندارد'}\n"
            f"🆔 {user.id}\n"
            f"📅 {message.date}"
        )
        
        if message.caption:
            caption += f"\n💬 توضیحات: {message.caption}"
        
        await context.bot.send_photo(
            chat_id=OWNER_CHAT_ID,
            photo=message.photo[-1].file_id,
            caption=caption
        )

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش پیام‌های صوتی"""
        user = update.effective_user
        message = update.message
        
        # ارسال پاسخ خودکار
        await message.reply_text(WELCOME_MESSAGE)
        
        # ارسال پیام صوتی به مالک
        caption = (
            f"🎤 پیام صوتی جدید از:\n"
            f"👤 {user.first_name} {user.last_name or ''}\n"
            f"📱 @{user.username or 'ندارد'}\n"
            f"🆔 {user.id}\n"
            f"📅 {message.date}\n"
            f"⏱️ مدت: {message.voice.duration} ثانیه"
        )
        
        await context.bot.send_voice(
            chat_id=OWNER_CHAT_ID,
            voice=message.voice.file_id,
            caption=caption
        )

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل‌ها"""
        user = update.effective_user
        message = update.message
        
        # ارسال پاسخ خودکار
        await message.reply_text(WELCOME_MESSAGE)
        
        # ارسال فایل به مالک
        caption = (
            f"📎 فایل جدید از:\n"
            f"👤 {user.first_name} {user.last_name or ''}\n"
            f"📱 @{user.username or 'ندارد'}\n"
            f"🆔 {user.id}\n"
            f"📅 {message.date}\n"
            f"📄 نام فایل: {message.document.file_name or 'نامشخص'}"
        )
        
        if message.caption:
            caption += f"\n💬 توضیحات: {message.caption}"
        
        await context.bot.send_document(
            chat_id=OWNER_CHAT_ID,
            document=message.document.file_id,
            caption=caption
        )

    async def handle_connection_issue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش گزینه قطع اینترنت"""
        user = update.effective_user
        message = update.message
        
        response_text = """🔴 ما داریم زیرساخت رو به‌روزرسانی می‌کنیم
        
حواست باشه کانال باشه برای اپدیت سابسکریپشن
        
📢 کانال ما: @FreeNet2Box"""
        
        await message.reply_text(response_text, reply_markup=get_main_menu())
        
        # ارسال به مالک
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"🔴 درخواست بررسی قطعی از:\n"
                 f"👤 {user.first_name} {user.last_name or ''}\n"
                 f"📱 @{user.username or 'ندارد'}\n"
                 f"🆔 {user.id}"
        )

    async def handle_renewal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش گزینه تمدید اکانت"""
        user = update.effective_user
        message = update.message
        
        response_text = """🔄 برای تمدید اکانت خود به پشتیبانی مراجعه کنید:
        
👨‍💻 پشتیبانی: @freeNetBoxSupport
        
پس از کلیک روی لینک بالا، اطلاعات اکانت خود را ارسال کنید."""
        
        await message.reply_text(response_text, reply_markup=get_main_menu())
        
        # ارسال به مالک
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"🔄 درخواست تمدید اکانت از:\n"
                 f"👤 {user.first_name} {user.last_name or ''}\n"
                 f"📱 @{user.username or 'ندارد'}\n"
                 f"🆔 {user.id}"
        )

    async def handle_channel_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش گزینه لینک کانال"""
        user = update.effective_user
        message = update.message
        
        response_text = """📢 لینک کانال ما:
        
🔗 @FreeNet2Box
        
در این کانال آخرین اخبار و به‌روزرسانی‌ها را دریافت خواهید کرد."""
        
        await message.reply_text(response_text, reply_markup=get_main_menu())
        
        # ارسال به مالک
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"📢 درخواست لینک کانال از:\n"
                 f"👤 {user.first_name} {user.last_name or ''}\n"
                 f"📱 @{user.username or 'ندارد'}\n"
                 f"🆔 {user.id}"
        )

    async def handle_buy_account(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش گزینه خرید اکانت"""
        user = update.effective_user
        message = update.message
        
        plans_text = get_account_plans()
        
        await message.reply_text(plans_text, reply_markup=get_main_menu())
        
        # ارسال به مالک
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"💰 درخواست خرید اکانت از:\n"
                 f"👤 {user.first_name} {user.last_name or ''}\n"
                 f"📱 @{user.username or 'ندارد'}\n"
                 f"🆔 {user.id}"
        )

    async def handle_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش گزینه انصراف"""
        try:
            user = update.effective_user
            
            cancel_text = """❌ عملیات لغو شد.
            
🏠 به منوی اصلی بازگشتید.
لطفاً گزینه مورد نظر خود را انتخاب کنید:"""
            
            await update.message.reply_text(
                cancel_text,
                reply_markup=get_main_menu()
            )
            
            # ثبت لاگ
            logger.info(f"کاربر {user.first_name} ({user.id}) عملیات را لغو کرد")
            
            # اطلاع به مالک (اختیاری)
            try:
                await context.bot.send_message(
                    chat_id=OWNER_CHAT_ID,
                    text=f"❌ کاربر عملیات را لغو کرد:\n"
                         f"👤 {user.first_name} {user.last_name or ''}\n"
                         f"📱 @{user.username or 'ندارد'}\n"
                         f"🆔 {user.id}"
                )
            except Exception as e:
                logger.error(f"خطا در ارسال پیام لغو به مالک: {e}")
                
        except Exception as e:
            logger.error(f"خطا در handle_cancel: {e}")
            try:
                await update.message.reply_text(
                    "❌ عملیات لغو شد. به منوی اصلی بازگشتید:",
                    reply_markup=get_main_menu()
                )
            except Exception as inner_e:
                logger.error(f"خطا در ارسال پیام پشتیبان انصراف: {inner_e}")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش خطاها"""
        logger.error(f"خطا در به‌روزرسانی {update}: {context.error}")
        
        # اگر خطایی رخ داد، سعی کن پیام دوستانه‌ای به کاربر ارسال کنی
        try:
            if update and update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="⚠️ خطای موقتی رخ داد. لطفاً دوباره امتحان کنید.",
                    reply_markup=get_main_menu()
                )
        except Exception as e:
            logger.error(f"خطا در ارسال پیام خطا: {e}")

    def run(self):
        """اجرای ربات"""
        # اضافه کردن هندلر خطا
        self.application.add_error_handler(self.error_handler)
        
        print("🤖 ربات تلگرام شروع به کار کرد...")
        print("🔄 در حال انتظار برای پیام‌ها...")
        
        # اجرای ربات
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """تابع اصلی"""
    # بررسی تنظیمات
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ لطفاً ابتدا توکن ربات را در فایل config.py تنظیم کنید")
        return
    
    if OWNER_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ لطفاً ابتدا Chat ID خود را در فایل config.py تنظیم کنید")
        return
    
    # ایجاد و اجرای ربات
    bot = TelegramBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n⏹️ ربات متوقف شد.")
    except Exception as e:
        print(f"❌ خطا در اجرای ربات: {e}")

if __name__ == "__main__":
    main() 