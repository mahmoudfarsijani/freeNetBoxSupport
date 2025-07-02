#!/bin/bash

echo "⏹️  متوقف کردن ربات تلگرام..."

# بررسی وجود فایل PID
if [ -f "bot.pid" ]; then
    BOT_PID=$(cat bot.pid)
    
    # بررسی آیا process در حال اجرا است
    if ps -p $BOT_PID > /dev/null; then
        kill $BOT_PID
        echo "✅ ربات با PID $BOT_PID متوقف شد"
        rm bot.pid
    else
        echo "⚠️  ربات با PID $BOT_PID در حال اجرا نیست"
        rm bot.pid
    fi
else
    echo "❌ فایل PID یافت نشد. ربات احتمالاً در حال اجرا نیست"
    
    # جستجوی manual برای process ربات
    BOT_PID=$(pgrep -f "python3 run.py")
    if [ ! -z "$BOT_PID" ]; then
        echo "🔍 ربات یافت شد با PID: $BOT_PID"
        kill $BOT_PID
        echo "✅ ربات متوقف شد"
    else
        echo "❌ هیچ ربات فعالی یافت نشد"
    fi
fi 