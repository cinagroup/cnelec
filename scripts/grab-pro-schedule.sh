#!/bin/bash
# 定时抢购启动脚本
# 使用方法：bash grab-pro-schedule.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_TIME="10:00"
LOG_FILE="/tmp/grab-pro-schedule.log"

# 配置账号信息（请根据实际情况修改）
export BIGMODEL_EMAIL="cinagroup"
export BIGMODEL_PASSWORD="qq123456789"
export PLAN_TYPE="Pro"

echo "⏰ bigmodel.cn GLM-Coding Pro 抢购定时任务"
echo "📅 目标时间：明天 $TARGET_TIME"
echo "👤 账号：$BIGMODEL_EMAIL"
echo ""

# 计算明天 10 点的 Unix 时间戳
TARGET_DATE=$(date -d "tomorrow $TARGET_TIME" +%s)
CURRENT_DATE=$(date +%s)
WAIT_SECONDS=$((TARGET_DATE - CURRENT_DATE))

echo "⏳ 等待 $WAIT_SECONDS 秒（约 $((WAIT_SECONDS / 3600)) 小时）"
echo "📝 日志将保存到：$LOG_FILE"
echo ""

# 后台等待并执行
(
    sleep $WAIT_SECONDS
    echo "========================================" >> $LOG_FILE
    echo "⏰ [$(date '+%Y-%m-%d %H:%M:%S')] 开始执行抢购" >> $LOG_FILE
    
    # 执行抢购脚本
    cd "$SCRIPT_DIR"
    python3 grab-pro.py 2>&1 | tee -a $LOG_FILE
    
    echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] 执行完成" >> $LOG_FILE
) &

SCHEDULER_PID=$!
echo "✅ 定时任务已启动（后台进程）"
echo "   进程 ID: $SCHEDULER_PID"
echo ""
echo "💡 提示："
echo "   - 查看日志：tail -f $LOG_FILE"
echo "   - 立即执行：bash $0 --now"
echo "   - 取消任务：kill $SCHEDULER_PID"

# 保存 PID 以便取消
echo $SCHEDULER_PID > /tmp/grab-pro-scheduler.pid
