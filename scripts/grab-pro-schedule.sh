#!/bin/bash
# 定时抢购启动脚本
# 使用方法：bash grab-pro-schedule.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_TIME="10:00"
LOG_FILE="/tmp/grab-pro-schedule.log"

echo "⏰ bigmodel.cn Pro 抢购定时任务"
echo "📅 目标时间：明天 $TARGET_TIME"
echo ""

# 计算明天 10 点的 Unix 时间戳
TARGET_DATE=$(date -d "tomorrow $TARGET_TIME" +%s)
CURRENT_DATE=$(date +%s)
WAIT_SECONDS=$((TARGET_DATE - CURRENT_DATE))

echo "⏳ 等待 $WAIT_SECONDS 秒..."
echo "📝 日志将保存到：$LOG_FILE"
echo ""

# 后台等待并执行
(
    sleep $WAIT_SECONDS
    echo "⏰ [$ (date '+%Y-%m-%d %H:%M:%S')] 开始执行抢购" >> $LOG_FILE
    
    # 加载环境变量（如果有的话）
    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi
    
    # 执行抢购脚本
    cd "$SCRIPT_DIR"
    python3 grab-pro.py 2>&1 | tee -a $LOG_FILE
    
    echo "✅ [$ (date '+%Y-%m-%d %H:%M:%S')] 执行完成" >> $LOG_FILE
) &

echo "✅ 定时任务已启动（后台进程）"
echo "   进程 ID: $!"
echo ""
echo "💡 提示："
echo "   - 查看日志：tail -f $LOG_FILE"
echo "   - 立即执行：python3 grab-pro.py"
echo "   - 配置账号：export BIGMODEL_EMAIL=xxx BIGMODEL_PASSWORD=xxx"
