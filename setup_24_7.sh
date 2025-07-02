#!/bin/bash

echo "🤖 راه‌اندازی ربات 24/7"
echo "=" * 50

echo "🎯 چه کاری می‌خوای انجام بدی؟"
echo ""
echo "1️⃣  تنظیم لپ‌تاپ برای کار دائمی (ساده)"
echo "2️⃣  Deploy روی Railway.app (رایگان)"
echo "3️⃣  Deploy روی Render.com (رایگان)"
echo "4️⃣  نمایش همه گزینه‌ها"
echo "5️⃣  خروج"
echo ""

read -p "🔢 شماره گزینه رو وارد کن (1-5): " choice

case $choice in
    1)
        echo ""
        echo "⚙️  تنظیم لپ‌تاپ برای کار دائمی..."
        echo ""
        echo "🔧 دستورات مورد نیاز:"
        echo ""
        echo "# جلوگیری از خواب کامپیوتر (وقتی شارژر وصله)"
        echo "sudo pmset -c sleep 0"
        echo "sudo pmset -c displaysleep 10"
        echo ""
        echo "# یا از System Preferences:"
        echo "# System Preferences → Battery → Power Adapter"
        echo "# Turn display off after: 10 minutes"
        echo "# Prevent your Mac from automatically sleeping: ✓"
        echo ""
        echo "⚠️  نکات مهم:"
        echo "• لپ‌تاپ باید همیشه به برق وصل باشه"
        echo "• اینترنت باید قطع نشه"
        echo "• بهتره ventilation خوب داشته باشه"
        echo ""
        
        read -p "❓ می‌خوای این تنظیمات رو اعمال کنم؟ (y/N): " apply
        if [[ $apply =~ ^[Yy]$ ]]; then
            echo "🔄 اعمال تنظیمات..."
            sudo pmset -c sleep 0
            sudo pmset -c displaysleep 10
            echo "✅ تنظیمات اعمال شد!"
            echo "🚀 حالا ربات رو با ./install_service.sh نصب کن"
        fi
        ;;
        
    2)
        echo ""
        echo "🚂 Deploy روی Railway.app..."
        echo ""
        echo "📋 مراحل:"
        echo "1. نصب Railway CLI"
        echo "2. ایجاد اکانت رایگان"
        echo "3. Deploy پروژه"
        echo ""
        
        read -p "❓ ادامه می‌دی؟ (y/N): " continue
        if [[ $continue =~ ^[Yy]$ ]]; then
            python3 deploy_railway.py
        fi
        ;;
        
    3)
        echo ""
        echo "🎨 Deploy روی Render.com..."
        echo ""
        echo "📋 مراحل:"
        echo "1. ایجاد اکانت GitHub"
        echo "2. Push کردن پروژه"
        echo "3. Deploy روی Render"
        echo ""
        
        read -p "❓ ادامه می‌دی؟ (y/N): " continue
        if [[ $continue =~ ^[Yy]$ ]]; then
            python3 deploy_render.py
        fi
        ;;
        
    4)
        echo ""
        echo "🎯 همه گزینه‌های 24/7:"
        echo ""
        echo "🏠 محلی (لپ‌تاپ):"
        echo "   ✅ سریع و آسان"
        echo "   ❌ وابسته به لپ‌تاپ"
        echo "   ❌ مصرف برق"
        echo ""
        echo "☁️  سرویس‌های ابری رایگان:"
        echo ""
        echo "   🚂 Railway.app:"
        echo "   ✅ 500 ساعت رایگان در ماه"
        echo "   ✅ راه‌اندازی آسان"
        echo "   ✅ Auto-restart"
        echo ""
        echo "   🎨 Render.com:"
        echo "   ✅ 750 ساعت رایگان در ماه"
        echo "   ✅ از GitHub deploy می‌کنه"
        echo "   ❌ یکم پیچیده‌تر"
        echo ""
        echo "   🌿 Heroku:"
        echo "   ❌ دیگه رایگان نیست"
        echo ""
        echo "   🔷 VPS (پولی):"
        echo "   ✅ کنترل کامل"
        echo "   ✅ منابع بیشتر"
        echo "   ❌ ماهی 5-10 دلار"
        echo ""
        echo "💡 پیشنهاد: اگه تازه‌کاری، از Railway شروع کن!"
        ;;
        
    5)
        echo "👋 خداحافظ!"
        exit 0
        ;;
        
    *)
        echo "❌ گزینه نامعتبر!"
        ;;
esac

echo ""
echo "🤖 هر وقت سوال داشتی، بپرس!" 