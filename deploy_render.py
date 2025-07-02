#!/usr/bin/env python3
"""
اسکریپت deploy برای Render.com
سرویس رایگان دیگر برای اجرای ربات 24/7
"""

import os
import json

def create_render_files():
    """ایجاد فایل‌های مورد نیاز برای Render"""
    
    # 1. render.yaml
    render_config = """services:
  - type: web
    name: telegram-bot
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python3 run.py"
    plan: free
    autoDeploy: false
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: OWNER_CHAT_ID
        sync: false
"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_config)
    
    # 2. Dockerfile (اختیاری)
    dockerfile = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "run.py"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    print("✅ فایل‌های Render ایجاد شدند")
    print("📋 مراحل بعدی:")
    print("1. برو به https://render.com")
    print("2. اکانت بساز (رایگان)")
    print("3. پروژه رو به GitHub push کن")
    print("4. پروژه رو از GitHub import کن")
    print("5. متغیرهای BOT_TOKEN و OWNER_CHAT_ID رو تنظیم کن")

def create_git_setup():
    """راه‌اندازی Git برای push به GitHub"""
    
    gitignore = """# Environment
.env
.env.local

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Logs
*.log
bot.pid

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore)
    
    print("\n🔧 راه‌اندازی Git:")
    print("1. git init")
    print("2. git add .")
    print('3. git commit -m "Initial commit"')
    print("4. git remote add origin https://github.com/username/repo.git")
    print("5. git push -u origin main")

def main():
    """تابع اصلی"""
    print("🎨 Render.com Deployment")
    print("=" * 40)
    print("🆓 سرویس رایگان دیگر برای اجرای ربات 24/7")
    print("=" * 40)
    
    # بررسی وجود فایل‌های ضروری
    if not os.path.exists('.env'):
        print("❌ فایل .env یافت نشد!")
        print("لطفاً ابتدا BOT_TOKEN و OWNER_CHAT_ID را تنظیم کنید")
        return
    
    # ایجاد فایل‌های Render
    create_render_files()
    create_git_setup()
    
    print("\n💡 راهنمای کامل:")
    print("🌐 https://render.com/docs/deploy-python")

if __name__ == "__main__":
    main() 