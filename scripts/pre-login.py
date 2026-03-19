#!/usr/bin/env python3
"""
bigmodel.cn 预登录脚本 - 提前登录保持会话
用于抢购前准备
"""

import os
import sys
from playwright.sync_api import sync_playwright

BIGMODEL_EMAIL = os.getenv("BIGMODEL_EMAIL", "")
BIGMODEL_PASSWORD = os.getenv("BIGMODEL_PASSWORD", "")

def pre_login():
    """提前登录并保存 Cookie"""
    print("🔐 bigmodel.cn 预登录脚本")
    print("=" * 50)
    
    if not BIGMODEL_EMAIL or not BIGMODEL_PASSWORD:
        print("❌ 错误：请设置 BIGMODEL_EMAIL 和 BIGMODEL_PASSWORD")
        sys.exit(1)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            # 访问登录页面
            print("📄 访问登录页面...")
            page.goto('https://bigmodel.cn/', timeout=30000)
            page.wait_for_timeout(3000)
            
            # 查找登录入口
            print("🔍 查找登录入口...")
            login_triggers = [
                'text=登录',
                'text=Login',
                'text=API Login',
                '.login-btn',
                '[class*="login"]'
            ]
            
            for trigger in login_triggers:
                try:
                    if page.is_visible(trigger):
                        print(f"✅ 找到登录入口：{trigger}")
                        page.click(trigger)
                        page.wait_for_timeout(3000)
                        break
                except:
                    continue
            
            # 填写登录表单
            print("📝 填写登录信息...")
            
            # 尝试多种表单选择器
            email_inputs = ['input[type="email"]', 'input[type="text"]', '#email', '.email-input']
            password_inputs = ['input[type="password"]', '#password', '.password-input']
            
            for email_selector in email_inputs:
                try:
                    if page.is_visible(email_selector):
                        page.fill(email_selector, BIGMODEL_EMAIL)
                        print(f"✅ 填写邮箱：{email_selector}")
                        break
                except:
                    continue
            
            for pwd_selector in password_inputs:
                try:
                    if page.is_visible(pwd_selector):
                        page.fill(pwd_selector, BIGMODEL_PASSWORD)
                        print(f"✅ 填写密码：{pwd_selector}")
                        break
                except:
                    continue
            
            # 点击登录按钮
            print("🔑 提交登录...")
            submit_buttons = ['button[type="submit"]', '.submit-btn', 'text=登录', 'text=Login']
            
            for btn in submit_buttons:
                try:
                    if page.is_visible(btn):
                        page.click(btn)
                        print(f"✅ 点击登录按钮：{btn}")
                        page.wait_for_timeout(5000)
                        break
                except:
                    continue
            
            # 检查登录状态
            page.wait_for_timeout(3000)
            current_url = page.url
            print(f"📍 当前 URL: {current_url}")
            
            # 截图确认
            page.screenshot(path='/tmp/login-result.png')
            print("✅ 登录截图：/tmp/login-result.png")
            
            # 保存 Cookie
            cookies = context.cookies()
            import json
            with open('/tmp/bigmodel_cookies.json', 'w') as f:
                json.dump(cookies, f, indent=2)
            print("✅ Cookie 已保存：/tmp/bigmodel_cookies.json")
            
            print("\n💡 提示：")
            print("   - 如需手动登录，请在浏览器中完成")
            print("   - 抢购脚本会自动检测登录状态")
            print("   - 保持浏览器打开可以提高抢购成功率")
            
        except Exception as e:
            print(f"❌ 错误：{e}")
            page.screenshot(path='/tmp/login-error.png')
            import traceback
            traceback.print_exc()
        
        finally:
            # 保持浏览器打开供用户确认（可选）
            print("\n⏸️  浏览器将在 10 秒后关闭...")
            page.wait_for_timeout(10000)
            browser.close()

if __name__ == "__main__":
    pre_login()
