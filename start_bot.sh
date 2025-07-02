#!/bin/bash

echo "🚀 شروع ربات تلگرام..."

# بررسی وجود فایل .env
if [ ! -f ".env" ]; then
    echo "❌ فایل .env یافت نشد!"
    echo "لطفاً ابتدا BOT_TOKEN و OWNER_CHAT_ID را تنظیم کنید"
    exit 1
fi

# شروع ربات در پس‌زمینه
nohup python3 run.py > bot.log 2>&1 &
BOT_PID=$!

echo "✅ ربات با موفقیت شروع شد!"
echo "📝 PID ربات: $BOT_PID"
echo "📋 فایل لاگ: bot.log"
echo "⏹️  برای متوقف کردن: kill $BOT_PID"

# ذخیره PID در فایل
echo $BOT_PID > bot.pid

echo ""
echo "🔍 برای مشاهده لاگ‌ها: tail -f bot.log"
echo "📱 ربات آماده پاسخ‌گویی است!" 