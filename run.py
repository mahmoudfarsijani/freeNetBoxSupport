#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ربات تلگرام خودران - اجرای 24/7
"""

import time
import logging
import sys
import os
from telegram_bot import main
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیم logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def check_config():
    """بررسی تنظیمات ربات"""
    bot_token = None
    owner_chat_id = None
    
    # اول از متغیرهای محیطی (.env) چک کن
    bot_token = os.getenv('BOT_TOKEN')
    owner_chat_id = os.getenv('OWNER_CHAT_ID')
    
    # اگر نبود، از config.py چک کن
    if not bot_token or not owner_chat_id:
        try:
            from config import BOT_TOKEN, OWNER_CHAT_ID
            if not bot_token:
                bot_token = BOT_TOKEN
            if not owner_chat_id:
                owner_chat_id = OWNER_CHAT_ID
        except ImportError:
            pass
    
    # بررسی نهایی
    if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ BOT_TOKEN تنظیم نشده!")
        logger.error("لطفاً در فایل .env یا config.py تنظیم کنید")
        return False
        
    if not owner_chat_id or owner_chat_id == "YOUR_CHAT_ID_HERE":
        logger.error("❌ OWNER_CHAT_ID تنظیم نشده!")
        logger.error("لطفاً در فایل .env یا config.py تنظیم کنید")
        return False
    
    # تنظیم متغیرهای محیطی برای استفاده در telegram_bot.py
    os.environ['BOT_TOKEN'] = str(bot_token)
    os.environ['OWNER_CHAT_ID'] = str(owner_chat_id)
    
    return True

def run_bot_forever():
    """اجرای ربات با restart خودکار"""
    restart_count = 0
    max_restarts = 50  # حداکثر تعداد restart در ساعت
    restart_window = 3600  # 1 ساعت (ثانیه)
    restart_times = []
    
    while True:
        try:
            logger.info("🚀 شروع ربات تلگرام...")
            
            # بررسی تنظیمات
            if not check_config():
                logger.error("❌ تنظیمات ناقص - انتظار 60 ثانیه...")
                time.sleep(60)
                continue
            
            # اجرای ربات
            main()
            
        except KeyboardInterrupt:
            logger.info("⏹️ ربات توسط کاربر متوقف شد")
            break
            
        except Exception as e:
            # مدیریت restart counter
            current_time = time.time()
            restart_times = [t for t in restart_times if current_time - t < restart_window]
            restart_times.append(current_time)
            
            if len(restart_times) > max_restarts:
                logger.error(f"❌ تعداد زیاد restart در ساعت گذشته: {len(restart_times)}")
                logger.error("⏸️ متوقف شدن برای 1 ساعت...")
                time.sleep(3600)
                restart_times.clear()
                continue
            
            restart_count += 1
            wait_time = min(30 * restart_count, 300)  # حداکثر 5 دقیقه
            
            logger.error(f"❌ خطا در ربات: {str(e)}")
            logger.info(f"🔄 restart #{restart_count} در {wait_time} ثانیه...")
            
            time.sleep(wait_time)
            
        except SystemExit:
            logger.info("🛑 خروج سیستمی")
            break

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("🤖 سرویس ربات تلگرام خودران")
    logger.info("=" * 50)
    
    try:
        run_bot_forever()
    except Exception as e:
        logger.error(f"💥 خطای کلی: {str(e)}")
        sys.exit(1) 