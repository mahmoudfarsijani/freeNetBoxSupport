#!/usr/bin/env python3
"""
اسکریپت deploy برای Railway.app
سرویس رایگان برای اجرای ربات 24/7
"""

import os
import subprocess
import sys

def create_railway_files():
    """ایجاد فایل‌های مورد نیاز برای Railway"""
    
    # 1. Procfile
    with open('Procfile', 'w') as f:
        f.write('web: python3 run.py\n')
    
    # 2. runtime.txt 
    with open('runtime.txt', 'w') as f:
        f.write('python-3.9.6\n')
    
    # 3. railway.json
    railway_config = """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python3 run.py",
    "restartPolicyType": "ALWAYS"
  }
}"""
    
    with open('railway.json', 'w') as f:
        f.write(railway_config)
    
    # 4. .gitignore
    gitignore = """# Environment
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
pip-log.txt
pip-delete-this-directory.txt

# Logs
*.log
bot.pid
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore)
    
    print("✅ فایل‌های Railway ایجاد شدند")

def check_railway_cli():
    """بررسی نصب Railway CLI"""
    try:
        result = subprocess.run(['railway', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Railway CLI نصب است: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Railway CLI نصب نیست")
    return False

def install_railway_cli():
    """نصب Railway CLI"""
    print("📦 نصب Railway CLI...")
    
    # macOS/Linux
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        cmd = 'curl -fsSL https://railway.app/install.sh | sh'
        print(f"🔧 اجرای: {cmd}")
        print("⚠️  لطفاً دستور زیر را در ترمینال اجرا کنید:")
        print(f"   {cmd}")
        print("سپس دوباره این اسکریپت را اجرا کنید")
        return False
    
    print("❌ سیستم عامل پشتیبانی نمی‌شود")
    return False

def setup_railway_project():
    """راه‌اندازی پروژه Railway"""
    if not check_railway_cli():
        return install_railway_cli()
    
    print("🚀 راه‌اندازی پروژه Railway...")
    
    # Login
    print("🔐 وارد شدن به Railway...")
    subprocess.run(['railway', 'login'])
    
    # Create project
    print("📁 ایجاد پروژه جدید...")
    subprocess.run(['railway', 'init'])
    
    # Set environment variables
    print("⚙️  تنظیم متغیرهای محیطی...")
    
    # خواندن از .env
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    subprocess.run(['railway', 'variables', 'set', f'{key}={value}'])
                    print(f"✅ {key} تنظیم شد")
    
    # Deploy
    print("🚀 Deploy پروژه...")
    subprocess.run(['railway', 'up'])
    
    print("\n🎉 ربات شما روی Railway deploy شد!")
    print("🌐 حالا 24/7 کار می‌کند!")
    print("📊 برای مشاهده لاگ‌ها: railway logs")
    print("⚙️  برای تنظیمات: https://railway.app/dashboard")

def main():
    """تابع اصلی"""
    print("🚂 Railway.app Deployment")
    print("=" * 40)
    print("🆓 سرویس رایگان برای اجرای ربات 24/7")
    print("=" * 40)
    
    # بررسی وجود فایل‌های ضروری
    if not os.path.exists('.env'):
        print("❌ فایل .env یافت نشد!")
        print("لطفاً ابتدا BOT_TOKEN و OWNER_CHAT_ID را تنظیم کنید")
        return
    
    # ایجاد فایل‌های Railway
    create_railway_files()
    
    # راه‌اندازی
    setup_railway_project()

if __name__ == "__main__":
    main() 