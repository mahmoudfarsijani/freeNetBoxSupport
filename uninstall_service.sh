#!/bin/bash

echo "🗑️  حذف سرویس ربات تلگرام..."
echo "=" * 50

# مسیر فایل plist
PLIST_FILE="$HOME/Library/LaunchAgents/com.telegram.bot.plist"

# بررسی وجود سرویس
if [ ! -f "$PLIST_FILE" ]; then
    echo "❌ سرویس نصب نشده است"
    exit 1
fi

# توقف سرویس
echo "⏹️  توقف سرویس..."
launchctl stop com.telegram.bot 2>/dev/null || true

# حذف سرویس از launchctl
echo "📤 حذف سرویس از سیستم..."
launchctl unload "$PLIST_FILE" 2>/dev/null || true

# حذف فایل plist
echo "🗑️  حذف فایل سرویس..."
rm -f "$PLIST_FILE"

# پیش‌نهاد حذف لاگ‌ها
echo ""
read -p "❓ آیا می‌خواهید لاگ‌ها را هم حذف کنید؟ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f bot.log bot_error.log bot.pid
    echo "🗑️  لاگ‌ها حذف شدند"
fi

echo ""
echo "=" * 50
echo "✅ سرویس با موفقیت حذف شد!"
echo ""
echo "💡 اگر می‌خواهید ربات را دستی اجرا کنید:"
echo "   python3 run.py"
echo "   یا"
echo "   ./start_bot.sh"

# بررسی وضعیت
echo ""
echo "🔍 وضعیت سرویس:"
if launchctl list | grep -q telegram; then
    echo "⚠️  هنوز برخی فرآیندها در حال اجرا هستند"
else
    echo "✅ سرویس کاملاً حذف شد"
fi 