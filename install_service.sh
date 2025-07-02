#!/bin/bash

echo "🚀 نصب سرویس ربات تلگرام خودران..."
echo "=" * 50

# بررسی macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ این اسکریپت فقط برای macOS طراحی شده است"
    exit 1
fi

# بررسی وجود فایل .env
if [ ! -f ".env" ]; then
    echo "❌ فایل .env یافت نشد!"
    echo "📝 لطفاً ابتدا فایل .env را ایجاد کنید:"
    echo "   BOT_TOKEN=your_bot_token_here"
    echo "   OWNER_CHAT_ID=your_chat_id_here"
    exit 1
fi

# مسیر فعلی
CURRENT_DIR=$(pwd)
PLIST_FILE="$HOME/Library/LaunchAgents/com.telegram.bot.plist"

echo "📁 مسیر پروژه: $CURRENT_DIR"

# کپی فایل plist به مسیر صحیح
echo "📄 کپی فایل سرویس..."
mkdir -p "$HOME/Library/LaunchAgents"

# تنظیم مسیر صحیح در فایل plist
sed "s|/Users/muti/Desktop/coding/projB|$CURRENT_DIR|g" com.telegram.bot.plist > "$PLIST_FILE"

# تنظیم مجوزها
chmod 644 "$PLIST_FILE"

echo "✅ فایل سرویس نصب شد: $PLIST_FILE"

# لود سرویس
echo "🔄 راه‌اندازی سرویس..."
launchctl load "$PLIST_FILE" 2>/dev/null || true

# شروع سرویس
echo "▶️ شروع سرویس..."
launchctl start com.telegram.bot

echo ""
echo "=" * 50
echo "✅ نصب سرویس کامل شد!"
echo ""
echo "📋 دستورات مدیریت سرویس:"
echo "   شروع:     launchctl start com.telegram.bot"
echo "   توقف:      launchctl stop com.telegram.bot"
echo "   حذف:       launchctl unload $PLIST_FILE"
echo "   وضعیت:     launchctl list | grep telegram"
echo ""
echo "📂 لاگ‌ها:"
echo "   عادی:      $CURRENT_DIR/bot.log"
echo "   خطاها:     $CURRENT_DIR/bot_error.log"
echo ""
echo "🤖 ربات حالا خودکار کار می‌کند و بعد از restart سیستم دوباره شروع می‌شود!"

# نمایش وضعیت
sleep 2
echo ""
echo "🔍 وضعیت فعلی سرویس:"
launchctl list | grep telegram || echo "سرویس در حال راه‌اندازی..." 