#!/usr/bin/env python3
"""
bigmodel.cn GLM-Coding Pro 版本限量抢购脚本
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
TARGET_URL = "https://bigmodel.cn/glm-coding"  # GLM-Coding 页面
PLAN_TYPE = os.getenv("PLAN_TYPE", "Pro")  # 套餐类型：Pro 或 Lite
TARGET_TIME = "10:00"  # 目标时间

def grab_pro():
    """执行抢购 GLM-Coding Pro 版本"""
    print(f"🎯 开始抢购 bigmodel.cn GLM-Coding {PLAN_TYPE} 版本")
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
                '--disable-dev-shm-usage'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = context.new_page()
        
        try:
            # 1. 访问 GLM-Coding 页面
            print(f"📄 访问：{TARGET_URL}")
            page.goto(TARGET_URL, timeout=30000, wait_until='networkidle')
            page.wait_for_timeout(3000)  # 等待动态内容加载
            
            # 截图保存
            page.screenshot(path='/tmp/grab-start.png')
            print("✅ 页面截图：/tmp/grab-start.png")
            
            # 2. 检查是否已登录
            print("🔐 检查登录状态...")
            
            # 尝试查找登录按钮
            if page.is_visible('text=API Login') or page.is_visible('text=登录'):
                print("⚠️  未登录，需要先手动登录")
                print("💡 建议：先在浏览器中手动登录，保持会话")
                page.screenshot(path='/tmp/grab-need-login.png')
                
                # 尝试点击登录
                login_buttons = ['text=登录', 'text=Login', 'text=API Login', '.login-btn']
                for btn in login_buttons:
                    try:
                        if page.is_visible(btn):
                            page.click(btn)
                            print(f"✅ 点击登录按钮：{btn}")
                            page.wait_for_timeout(5000)
                            break
                    except:
                        continue
            
            # 3. 查找并点击"即刻订阅"或"特惠订阅"按钮
            print(f"💎 查找 {PLAN_TYPE} 套餐订阅按钮...")
            
            # 先查找 Pro 套餐卡片
            if PLAN_TYPE.lower() == "pro":
                plan_selectors = [
                    'text=Pro',
                    '.plan-card:has-text("Pro")',
                    '[class*="Pro"]',
                    '[class*="pro"]'
                ]
                
                for selector in plan_selectors:
                    try:
                        if page.is_visible(selector):
                            print(f"✅ 找到 Pro 套餐：{selector}")
                            break
                    except:
                        continue
            
            # 点击订阅按钮
            subscribe_buttons = [
                'text=即刻订阅',
                'text=特惠订阅',
                'text=继续订阅',
                'text=立即订阅',
                '.subscribe-btn',
                '.buy-btn'
            ]
            
            for btn in subscribe_buttons:
                try:
                    if page.is_visible(btn):
                        print(f"✅ 点击订阅按钮：{btn}")
                        page.click(btn)
                        page.wait_for_timeout(3000)
                        break
                except:
                    continue
            
            # 4. 选择连续包季选项（如果存在）
            print("📅 查找连续包季选项...")
            season_options = [
                'text=连续包季',
                'text=连续包季 9 折',
                '[class*="season"]',
                '[class*="quarter"]'
            ]
            
            for opt in season_options:
                try:
                    if page.is_visible(opt):
                        print(f"✅ 选择：{opt}")
                        page.click(opt)
                        page.wait_for_timeout(1000)
                        break
                except:
                    continue
            
            # 5. 确认购买/去支付
            print("💳 确认购买...")
            confirm_buttons = [
                'text=确认购买',
                'text=去支付',
                'text=立即购买',
                'text=确认下单',
                '.confirm-btn',
                '.checkout-btn'
            ]
            
            for btn in confirm_buttons:
                try:
                    if page.is_visible(btn):
                        print(f"✅ 点击确认：{btn}")
                        page.click(btn)
                        page.wait_for_timeout(3000)
                        break
                except:
                    continue
            
            # 6. 截图保存最终状态
            page.wait_for_timeout(2000)
            page.screenshot(path='/tmp/grab-result.png')
            print("✅ 抢购完成！截图：/tmp/grab-result.png")
            
            # 7. 发送通知
            print("📬 请检查截图并完成支付...")
            
        except Exception as e:
            print(f"❌ 错误：{e}")
            page.screenshot(path='/tmp/grab-error.png')
            import traceback
            traceback.print_exc()
            
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
