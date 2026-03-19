#!/usr/bin/env python3
"""
bigmodel.cn GLM-Coding Pro 高并发抢购脚本
支持多次重试、并发请求、容错机制
"""

import os
import sys
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ========== 配置区 ==========
BIGMODEL_EMAIL = os.getenv("BIGMODEL_EMAIL", "cinagroup")
BIGMODEL_PASSWORD = os.getenv("BIGMODEL_PASSWORD", "qq123456789")
PLAN_TYPE = os.getenv("PLAN_TYPE", "Pro")
TARGET_URL = "https://bigmodel.cn/glm-coding"

# 抢购策略配置
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "50"))         # 最大重试次数
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "0.5"))      # 重试间隔（秒）
PAGE_TIMEOUT = int(os.getenv("PAGE_TIMEOUT", "15000"))    # 页面加载超时（毫秒）
CLICK_TIMEOUT = int(os.getenv("CLICK_TIMEOUT", "5000"))   # 点击超时（毫秒）
ENABLE_RANDOM_DELAY = os.getenv("ENABLE_RANDOM_DELAY", "true").lower() == "true"  # 是否启用随机延迟

def random_sleep(min_ms=100, max_ms=500):
    """随机延迟，避免被识别为机器人"""
    if ENABLE_RANDOM_DELAY:
        time.sleep(random.uniform(min_ms, max_ms) / 1000)

def grab_with_retry():
    """带重试机制的抢购"""
    print(f"🎯 bigmodel.cn GLM-Coding {PLAN_TYPE} 高并发抢购")
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 配置：")
    print(f"   最大重试：{MAX_RETRIES} 次")
    print(f"   重试间隔：{RETRY_DELAY} 秒")
    print(f"   页面超时：{PAGE_TIMEOUT}ms")
    print(f"   随机延迟：{'启用' if ENABLE_RANDOM_DELAY else '禁用'}")
    print("=" * 60)
    
    if not BIGMODEL_EMAIL or not BIGMODEL_PASSWORD:
        print("❌ 错误：请设置 BIGMODEL_EMAIL 和 BIGMODEL_PASSWORD")
        sys.exit(1)
    
    success = False
    last_error = None
    screenshots = []
    
    with sync_playwright() as p:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"\n🔄 第 {attempt}/{MAX_RETRIES} 次尝试...")
                
                # 启动浏览器（每次重试都新建浏览器实例，避免状态污染）
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-gpu',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-setuid-sandbox',
                        '--disable-web-security',
                        '--disable-features=IsolateOrigins,site-per-process'
                    ]
                )
                
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    bypass_csp=True
                )
                
                page = context.new_page()
                page.set_default_timeout(PAGE_TIMEOUT)
                
                # 步骤 1: 访问页面
                print(f"   📄 访问页面...")
                start_time = time.time()
                page.goto(TARGET_URL, wait_until='domcontentloaded', timeout=PAGE_TIMEOUT)
                
                # 等待关键元素出现
                try:
                    page.wait_for_selector('text=Pro', timeout=5000)
                except:
                    pass  # 继续尝试，可能页面还在加载
                
                load_time = time.time() - start_time
                print(f"   ✅ 页面加载完成 ({load_time:.2f}s)")
                
                # 步骤 2: 快速检查登录状态
                if attempt == 1:  # 只在第一次尝试检查登录
                    print(f"   🔐 检查登录状态...")
                    try:
                        if page.is_visible('text=API Login', timeout=2000):
                            print(f"   ⚠️  未登录，尝试登录...")
                            # 简化的快速登录
                            try:
                                page.fill('input[type="text"]', BIGMODEL_EMAIL)
                                page.fill('input[type="password"]', BIGMODEL_PASSWORD)
                                page.click('button[type="submit"]')
                                page.wait_for_timeout(3000)
                            except:
                                pass
                    except:
                        pass
                
                # 步骤 3: 查找并点击 Pro 套餐
                print(f"   💎 查找 {PLAN_TYPE} 套餐...")
                random_sleep(50, 200)
                
                # 多种选择器策略
                plan_selectors = [
                    f'text={PLAN_TYPE}',
                    f'[class*="{PLAN_TYPE.lower()}"]',
                    f'[data-plan*="{PLAN_TYPE.lower()}"]',
                    '.plan-card',
                    '.pricing-card'
                ]
                
                plan_found = False
                for selector in plan_selectors:
                    try:
                        if page.is_visible(selector, timeout=1000):
                            print(f"   ✅ 找到套餐：{selector}")
                            plan_found = True
                            break
                    except:
                        continue
                
                # 步骤 4: 点击订阅按钮（核心步骤）
                print(f"   🛒 点击订阅按钮...")
                random_sleep(50, 150)
                
                subscribe_buttons = [
                    'text=即刻订阅',
                    'text=特惠订阅',
                    'text=继续订阅',
                    'text=立即订阅',
                    'text=订阅',
                    '.subscribe-btn',
                    '.buy-btn',
                    '[class*="subscribe"]',
                    '[class*="buy"]'
                ]
                
                for btn in subscribe_buttons:
                    try:
                        if page.is_visible(btn, timeout=800):
                            page.click(btn, timeout=CLICK_TIMEOUT)
                            print(f"   ✅ 点击：{btn}")
                            random_sleep(100, 300)
                            break
                    except Exception as e:
                        continue
                
                # 步骤 5: 选择连续包季
                print(f"   📅 选择连续包季...")
                random_sleep(50, 150)
                
                season_options = [
                    'text=连续包季',
                    'text=连续包季 9 折',
                    '[class*="season"]',
                    '[class*="quarter"]'
                ]
                
                for opt in season_options:
                    try:
                        if page.is_visible(opt, timeout=800):
                            page.click(opt, timeout=CLICK_TIMEOUT)
                            print(f"   ✅ 选择：{opt}")
                            random_sleep(100, 200)
                            break
                    except:
                        continue
                
                # 步骤 6: 确认购买
                print(f"   💳 确认购买...")
                random_sleep(50, 150)
                
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
                        if page.is_visible(btn, timeout=800):
                            page.click(btn, timeout=CLICK_TIMEOUT)
                            print(f"   ✅ 点击确认：{btn}")
                            random_sleep(200, 500)
                            
                            # 检查是否成功到达支付页面
                            current_url = page.url
                            if 'pay' in current_url.lower() or 'order' in current_url.lower() or 'checkout' in current_url.lower():
                                print(f"   🎉 成功到达支付页面！")
                                success = True
                            break
                    except:
                        continue
                
                # 截图保存
                screenshot_path = f'/tmp/grab-attempt-{attempt}.png'
                page.screenshot(path=screenshot_path)
                screenshots.append(screenshot_path)
                
                # 检查是否成功
                current_url = page.url
                if 'pay' in current_url.lower() or 'order' in current_url.lower() or 'checkout' in current_url.lower() or success:
                    print(f"\n🎉🎉🎉 抢购成功！")
                    print(f"📍 当前 URL: {current_url}")
                    print(f"📸 截图：{screenshot_path}")
                    print(f"💳 请手动完成支付！")
                    success = True
                    browser.close()
                    break
                
                browser.close()
                
                # 失败后的延迟
                if attempt < MAX_RETRIES:
                    delay = RETRY_DELAY + random.uniform(0, 0.5)
                    print(f"   ⏳ 等待 {delay:.2f}秒后重试...")
                    time.sleep(delay)
                
            except PlaywrightTimeout as e:
                last_error = f"超时：{e}"
                print(f"   ⚠️  超时错误：{e}")
                try:
                    browser.close()
                except:
                    pass
                    
            except Exception as e:
                last_error = f"错误：{e}"
                print(f"   ❌ 错误：{e}")
                try:
                    browser.close()
                except:
                    pass
            
            # 每次尝试后短暂延迟，避免被封
            if attempt < MAX_RETRIES:
                time.sleep(random.uniform(0.2, 0.8))
    
    # 最终结果
    print("\n" + "=" * 60)
    if success:
        print("✅ 抢购成功！")
        print(f"📸 截图文件：{screenshots[-1] if screenshots else 'N/A'}")
        return 0
    else:
        print(f"❌ 抢购失败（{MAX_RETRIES}次尝试）")
        print(f"最后错误：{last_error}")
        if screenshots:
            print(f"最后截图：{screenshots[-1]}")
        return 1

if __name__ == "__main__":
    sys.exit(grab_with_retry())
