#!/bin/bash
# 抢购定时守护进程 - 确保准时执行，支持提前预热
# 使用方法：bash grab-pro-guardian.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_TIME="10:00"
PREWARM_MINUTES=5  # 提前预热分钟数
LOG_FILE="/tmp/grab-guardian.log"
PID_FILE="/tmp/grab-guardian.pid"

# 配置
export BIGMODEL_EMAIL="cinagroup"
export BIGMODEL_PASSWORD="qq123456789"
export PLAN_TYPE="Pro"
export MAX_RETRIES=100         # 守护模式下增加重试次数
export RETRY_DELAY=0.2         # 更快的重试间隔
export PAGE_TIMEOUT=30000      # 页面加载超时 30 秒
export CLICK_TIMEOUT=5000      # 点击超时 5 秒
export ENABLE_RANDOM_DELAY=true
export INSTANCE_COUNT=5        # 并发实例数

echo "🛡️  bigmodel.cn 抢购守护进程（高并发模式）"
echo "========================================"
echo "⏰ 目标时间：明天 $TARGET_TIME"
echo "🔥 预热时间：提前 $PREWARM_MINUTES 分钟"
echo "📦 并发实例：${INSTANCE_COUNT:-5}"
echo "📊 总尝试次数：$((INSTANCE_COUNT * MAX_RETRIES))"
echo "📝 日志：$LOG_FILE"
echo ""

# 计算时间
TARGET_DATE=$(date -d "tomorrow $TARGET_TIME" +%s)
CURRENT_DATE=$(date +%s)
WAIT_SECONDS=$((TARGET_DATE - CURRENT_DATE))

# 预热时间 = 目标时间 - 提前分钟数
PREWARM_SECONDS=$((WAIT_SECONDS - PREWARM_MINUTES * 60))

PREWARM_TIME_STR=$(date -d "@$((CURRENT_DATE + PREWARM_SECONDS))" '+%Y-%m-%d %H:%M:%S')
TARGET_TIME_STR=$(date -d "@$((CURRENT_DATE + WAIT_SECONDS))" '+%Y-%m-%d %H:%M:%S')

echo "📊 时间计算："
echo "   当前时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "   预热时间：$PREWARM_TIME_STR"
echo "   目标时间：$TARGET_TIME_STR"
echo "   距离预热：$PREWARM_SECONDS 秒（约 $((PREWARM_SECONDS / 3600)) 小时）"
echo "   距离目标：$WAIT_SECONDS 秒（约 $((WAIT_SECONDS / 3600)) 小时）"
echo ""

# 保存 PID
echo $$ > "$PID_FILE"
echo "📄 PID 文件：$PID_FILE"
echo ""

# 守护函数
run_grab() {
    local mode=$1
    echo "[$(date '+%H:%M:%S')] 开始抢购模式：$mode" >> "$LOG_FILE"
    
    cd "$SCRIPT_DIR"
    
    if [ "$mode" = "concurrent" ]; then
        # 并发模式：启动指定数量的实例
        bash grab-pro-concurrent.sh ${INSTANCE_COUNT:-5} 2>&1 | tee -a "$LOG_FILE"
    else
        # 单实例模式
        python3 grab-pro-fast.py 2>&1 | tee -a "$LOG_FILE"
    fi
    
    local exit_code=$?
    echo "[$(date '+%H:%M:%S')] 抢购结束 (exit code: $exit_code)" >> "$LOG_FILE"
    
    if [ $exit_code -eq 0 ]; then
        echo "[$(date '+%H:%M:%S')] 🎉 抢购成功！" >> "$LOG_FILE"
        # 发送通知（如果有）
        if command -v notify-send &> /dev/null; then
            notify-send "抢购成功" "bigmodel.cn Pro 版本抢购成功！"
        fi
        exit 0
    fi
    
    return $exit_code
}

# 主循环
echo "⏳ 进入守护模式..."
echo ""

# 检查是否需要预热
if [ $PREWARM_SECONDS -gt 0 ]; then
    echo "📌 等待预热时间..."
    sleep $PREWARM_SECONDS
fi

echo "🔥 开始预热（提前 $PREWARM_MINUTES 分钟）..."
echo "[$(date '+%H:%M:%S')] 开始预热" >> "$LOG_FILE"

# 预热：先运行一次单实例，保持连接
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://bigmodel.cn/glm-coding', timeout=10000)
    print('✅ 预热完成 - 页面已加载')
    browser.close()
" 2>&1 | tee -a "$LOG_FILE"

# 等待目标时间
REMAINING=$((WAIT_SECONDS - PREWARM_SECONDS))
if [ $REMAINING -gt 0 ]; then
    echo "⏳ 等待目标时间（剩余 $REMAINING 秒）..."
    sleep $REMAINING
fi

echo ""
echo "⏰ 时间到！开始抢购！"
echo "[$(date '+%H:%M:%S')] ⏰ 目标时间到达" >> "$LOG_FILE"

# 启动抢购（并发模式）
run_grab "concurrent"
RESULT=$?

# 如果失败，继续尝试
if [ $RESULT -ne 0 ]; then
    echo ""
    echo "⚠️  第一次尝试失败，继续重试..."
    
    # 继续重试 3 轮
    for i in 1 2 3; do
        echo "[$(date '+%H:%M:%S')] 第 $i 轮重试" >> "$LOG_FILE"
        echo "🔄 第 $i 轮重试..."
        
        sleep 5  # 等待 5 秒
        run_grab "concurrent"
        
        if [ $? -eq 0 ]; then
            exit 0
        fi
    done
fi

echo ""
echo "========================================"
echo "📊 执行完成"
echo "📝 完整日志：cat $LOG_FILE"
echo "📸 截图文件：ls -lh /tmp/grab-*.png"
