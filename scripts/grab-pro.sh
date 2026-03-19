#!/bin/bash
# bigmodel.cn Pro 版本限量抢购脚本
# 使用时间：明天 10:00

set -e

# ========== 配置区 ==========
# 请在使用前填写以下信息
BIGMODEL_EMAIL="${BIGMODEL_EMAIL:-}"        # 必填：账号邮箱
BIGMODEL_PASSWORD="${BIGMODEL_PASSWORD:-}"  # 必填：账号密码
TARGET_URL="https://bigmodel.cn/pricing"    # 目标页面
PRODUCT_SELECTOR=".pricing-card.pro"        # Pro 版本选择器（需根据实际页面调整）
BUY_BUTTON_SELECTOR="button.buy-btn"        # 购买按钮选择器
MAX_RETRIES=10                              # 最大重试次数
RETRY_INTERVAL=0.5                          # 重试间隔（秒）

# ========== 脚本主体 ==========
echo "🎯 bigmodel.cn Pro 抢购脚本"
echo "⏰ 目标时间：$(date -d 'tomorrow 10:00' '+%Y-%m-%d %H:%M:%S')"
echo "📦 配置检查..."

# 检查必填配置
if [ -z "$BIGMODEL_EMAIL" ] || [ -z "$BIGMODEL_PASSWORD" ]; then
    echo "❌ 错误：请配置 BIGMODEL_EMAIL 和 BIGMODEL_PASSWORD"
    echo "   方式 1: export BIGMODEL_EMAIL=xxx BIGMODEL_PASSWORD=xxx"
    echo "   方式 2: 编辑此脚本填写"
    exit 1
fi

# 创建抢购任务
cat > /tmp/grab-pro-task.json << EOF
{
  "url": "$TARGET_URL",
  "actions": [
    {"type": "wait", "selector": "input[type='email']", "timeout": 10000},
    {"type": "type", "selector": "input[type='email']", "value": "$BIGMODEL_EMAIL"},
    {"type": "type", "selector": "input[type='password']", "value": "$BIGMODEL_PASSWORD"},
    {"type": "click", "selector": "button[type='submit']"},
    {"type": "wait", "timeout": 3000},
    {"type": "click", "selector": "$PRODUCT_SELECTOR"},
    {"type": "click", "selector": "$BUY_BUTTON_SELECTOR"},
    {"type": "screenshot", "path": "/tmp/grab-result.png"}
  ]
}
EOF

echo "✅ 任务配置完成"
echo ""
echo "📋 使用方法："
echo "1. 设置环境变量："
echo "   export BIGMODEL_EMAIL='your@email.com'"
echo "   export BIGMODEL_PASSWORD='your_password'"
echo ""
echo "2. 手动立即执行："
echo "   bash $0 --run-now"
echo ""
echo "3. 定时明天 10 点执行："
echo "   bash $0 --schedule"
echo ""

# 处理参数
case "$1" in
  --run-now)
    echo "🚀 立即执行抢购..."
    # 使用 agent-browser 执行
    agent-browser run /tmp/grab-pro-task.json
    echo "✅ 执行完成，截图：/tmp/grab-result.png"
    ;;
  --schedule)
    echo "⏰ 设置定时任务..."
    # 使用 at 命令设置明天 10 点执行
    RUN_TIME=$(date -d 'tomorrow 10:00' '+%H:%M')
    echo "bash $0 --run-now | tee /tmp/grab-log.txt" | at $RUN_TIME
    echo "✅ 定时任务已设置：明天 $RUN_TIME"
    echo "   日志文件：/tmp/grab-log.txt"
    ;;
  *)
    echo "请指定参数：--run-now 或 --schedule"
    ;;
esac
