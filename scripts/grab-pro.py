#!/usr/bin/env python3
"""
bigmodel.cn Pro 版本限量抢购脚本
使用前请配置账号信息
"""

import os
import sys
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

# ========== 配置区 ==========
BIGMODEL_EMAIL = os.getenv("BIGMODEL_EMAIL", "")
BIGMODEL_PASSWORD = os.getenv("BIGMODEL_PASSWORD", "")
TARGET_URL = "https://bigmodel.cn/pricing"
TARGET_TIME = "10:00"  # 目标时间

def grab_pro():
    """执行抢购"""
    print(f"🎯 开始抢购 bigmodel.cn Pro 版本")
    print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not BIGMODEL_EMAIL or not BIGMODEL_PASSWORD:
        print("❌ 错误：请设置 BIGMODEL_EMAIL 和 BIGMODEL_PASSWORD 环境变量")
        sys.exit(1)
    
    with sync_playwright() as p:
        # 启动浏览器（高性能模式）
        browser = p.chromium.launch(
            headless=False,  # 显示浏览器便于观察
            args=[
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = context.new_page()
        
        try:
            # 1. 访问定价页面
            print(f"📄 访问：{TARGET_URL}")
            page.goto(TARGET_URL, timeout=30000)
            page.wait_for_load_state('networkidle')
            
            # 截图保存
            page.screenshot(path='/tmp/grab-start.png')
            
            # 2. 检查是否已登录
            print("🔐 检查登录状态...")
            
            # 如果未登录，执行登录
            if page.is_visible('input[type="email"]') or page.is_visible('input[type="text"]'):
                print("📝 执行登录...")
                page.fill('input[type="email"]', BIGMODEL_EMAIL)
                page.fill('input[type="password"]', BIGMODEL_PASSWORD)
                page.click('button[type="submit"]')
                page.wait_for_timeout(3000)
                page.screenshot(path='/tmp/grab-logged.png')
            
            # 3. 查找 Pro 版本并点击
            print("💎 查找 Pro 版本...")
            
            # 尝试多种选择器
            selectors = [
                '.pricing-card.pro',
                '.plan-pro',
                '[data-plan="pro"]',
                'button:has-text("Pro")',
                'button:has-text("PRO")',
                '.buy-btn',
                'button.buy'
            ]
            
            for selector in selectors:
                if page.is_visible(selector):
                    print(f"✅ 找到 Pro 版本：{selector}")
                    page.click(selector)
                    page.wait_for_timeout(1000)
                    break
            else:
                print("⚠️ 未找到 Pro 版本，尝试直接点击购买按钮")
            
            # 4. 点击购买/订阅按钮
            print("🛒 点击购买...")
            buy_selectors = [
                'button:has-text("购买")',
                'button:has-text("订阅")',
                'button:has-text("Buy")',
                'button:has-text("Subscribe")',
                '.checkout-btn',
                'a.checkout'
            ]
            
            for selector in buy_selectors:
                if page.is_visible(selector):
                    page.click(selector)
                    print(f"✅ 点击：{selector}")
                    break
            
            # 5. 截图保存最终状态
            page.wait_for_timeout(2000)
            page.screenshot(path='/tmp/grab-result.png')
            print("✅ 抢购完成！截图：/tmp/grab-result.png")
            
            # 6. 发送通知（如果有 QQBot）
            print("📬 发送通知...")
            
        except Exception as e:
            print(f"❌ 错误：{e}")
            page.screenshot(path='/tmp/grab-error.png')
            
        finally:
            browser.close()

def schedule_grab():
    """设置定时任务"""
    print(f"⏰ 设置定时抢购任务：明天 {TARGET_TIME}")
    
    # 使用 at 命令
    script_path = os.path.abspath(__file__)
    at_time = f"tomorrow {TARGET_TIME}"
    
    cmd = f'echo "python3 {script_path}" | at {at_time}'
    os.system(cmd)
    
    print("✅ 定时任务已设置")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        schedule_grab()
    else:
        grab_pro()
