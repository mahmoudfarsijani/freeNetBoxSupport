#!/bin/bash

echo "🤖 وضعیت ربات تلگرام"
echo "=" * 40

# بررسی سرویس launchctl
echo "🔍 بررسی سرویس خودکار:"
PLIST_FILE="$HOME/Library/LaunchAgents/com.telegram.bot.plist"

if [ -f "$PLIST_FILE" ]; then
    echo "✅ سرویس نصب شده است"
    
    if launchctl list | grep -q com.telegram.bot; then
        SERVICE_STATUS=$(launchctl list | grep com.telegram.bot)
        echo "🟢 وضعیت سرویس: در حال اجرا"
        echo "   $SERVICE_STATUS"
    else
        echo "🔴 وضعیت سرویس: متوقف"
    fi
else
    echo "❌ سرویس نصب نشده است"
fi

echo ""

# بررسی فرآیند دستی
echo "🔍 بررسی فرآیند دستی:"
MANUAL_PID=$(pgrep -f "python3.*run.py" | head -1)

if [ ! -z "$MANUAL_PID" ]; then
    echo "🟢 ربات دستی در حال اجرا (PID: $MANUAL_PID)"
    
    # نمایش اطلاعات فرآیند
    echo "   📊 اطلاعات فرآیند:"
    ps -p $MANUAL_PID -o pid,ppid,pcpu,pmem,etime,cmd | tail -1
else
    echo "❌ هیچ ربات دستی در حال اجرا نیست"
fi

echo ""

# بررسی فایل PID
echo "🔍 بررسی فایل PID:"
if [ -f "bot.pid" ]; then
    SAVED_PID=$(cat bot.pid)
    if ps -p $SAVED_PID > /dev/null 2>&1; then
        echo "✅ فایل PID معتبر: $SAVED_PID"
    else
        echo "⚠️  فایل PID نامعتبر: $SAVED_PID (فرآیند وجود ندارد)"
    fi
else
    echo "❌ فایل PID وجود ندارد"
fi

echo ""

# بررسی لاگ‌ها
echo "📊 وضعیت لاگ‌ها:"
if [ -f "bot.log" ]; then
    LOG_SIZE=$(du -h bot.log | cut -f1)
    LOG_LINES=$(wc -l < bot.log)
    echo "✅ لاگ عادی: $LOG_SIZE ($LOG_LINES خط)"
    
    # آخرین 3 خط لاگ
    echo "   📝 آخرین لاگ‌ها:"
    tail -3 bot.log | sed 's/^/      /'
else
    echo "❌ فایل لاگ وجود ندارد"
fi

if [ -f "bot_error.log" ]; then
    ERROR_SIZE=$(du -h bot_error.log | cut -f1)
    ERROR_LINES=$(wc -l < bot_error.log)
    echo "⚠️  لاگ خطا: $ERROR_SIZE ($ERROR_LINES خط)"
    
    if [ $ERROR_LINES -gt 0 ]; then
        echo "   🚨 آخرین خطاها:"
        tail -3 bot_error.log | sed 's/^/      /'
    fi
else
    echo "✅ هیچ خطایی ثبت نشده"
fi

echo ""

# بررسی تنظیمات
echo "⚙️  بررسی تنظیمات:"
if [ -f ".env" ]; then
    echo "✅ فایل .env موجود است"
    
    if grep -q "BOT_TOKEN=" .env && grep -q "OWNER_CHAT_ID=" .env; then
        echo "✅ متغیرهای اصلی تنظیم شده‌اند"
    else
        echo "⚠️  برخی متغیرها تنظیم نشده‌اند"
    fi
else
    echo "❌ فایل .env وجود ندارد"
fi

echo ""

# خلاصه وضعیت
echo "📋 خلاصه وضعیت:"

OVERALL_STATUS="❌ غیرفعال"

if launchctl list | grep -q com.telegram.bot; then
    OVERALL_STATUS="🟢 فعال (سرویس خودکار)"
elif [ ! -z "$MANUAL_PID" ]; then
    OVERALL_STATUS="🟡 فعال (دستی)"
fi

echo "   وضعیت کلی: $OVERALL_STATUS"

echo ""
echo "=" * 40

# راهنمای سریع
echo "💡 دستورات سریع:"
echo "   ./install_service.sh    - نصب سرویس خودکار"
echo "   ./start_bot.sh          - شروع دستی"
echo "   ./stop_bot.sh           - توقف دستی"
echo "   ./uninstall_service.sh  - حذف سرویس"
echo "   tail -f bot.log         - مشاهده لاگ‌های زنده" 