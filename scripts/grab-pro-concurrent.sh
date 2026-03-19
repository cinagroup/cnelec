#!/bin/bash
# bigmodel.cn 并发抢购脚本 - 多实例同时抢购
# 使用方法：bash grab-pro-concurrent.sh [实例数量]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTANCE_COUNT=${1:-3}  # 默认 3 个实例
LOG_FILE="/tmp/grab-concurrent.log"

# 配置账号信息
export BIGMODEL_EMAIL="cinagroup"
export BIGMODEL_PASSWORD="qq123456789"
export PLAN_TYPE="Pro"

# 抢购策略配置
export MAX_RETRIES=30          # 每个实例重试次数
export RETRY_DELAY=0.3         # 重试间隔（秒）
export PAGE_TIMEOUT=10000      # 页面加载超时（毫秒）
export CLICK_TIMEOUT=3000      # 点击超时（毫秒）
export ENABLE_RANDOM_DELAY=true

echo "🚀 bigmodel.cn GLM-Coding Pro 并发抢购"
echo "========================================"
echo "📦 实例数量：$INSTANCE_COUNT"
echo "📊 总尝试次数：$((INSTANCE_COUNT * MAX_RETRIES))"
echo "👤 账号：$BIGMODEL_EMAIL"
echo "📝 日志：$LOG_FILE"
echo ""

# 清理旧日志
> "$LOG_FILE"

# 启动多个实例
PIDS=()
for i in $(seq 1 $INSTANCE_COUNT); do
    echo "🚀 启动实例 #$i ..."
    
    (
        echo "[$(date '+%H:%M:%S')] 实例 #$i 启动" >> "$LOG_FILE"
        cd "$SCRIPT_DIR"
        python3 grab-pro-fast.py 2>&1 | tee -a "$LOG_FILE"
        EXIT_CODE=$?
        echo "[$(date '+%H:%M:%S')] 实例 #$i 结束 (exit code: $EXIT_CODE)" >> "$LOG_FILE"
        
        # 如果成功，创建标记文件
        if [ $EXIT_CODE -eq 0 ]; then
            touch /tmp/grab-success-instance-$i
            echo "[$(date '+%H:%M:%S')] 🎉 实例 #$i 抢购成功！" >> "$LOG_FILE"
        fi
    ) &
    
    PIDS+=($!)
    echo "   进程 ID: ${PIDS[-1]}"
done

echo ""
echo "⏳ 等待所有实例完成..."
echo ""

# 等待所有实例完成
SUCCESS=0
for i in "${!PIDS[@]}"; do
    wait ${PIDS[$i]}
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        SUCCESS=1
        echo "✅ 实例 $((i+1)) 完成（成功）"
    else
        echo "❌ 实例 $((i+1)) 完成（失败）"
    fi
done

echo ""
echo "========================================"

# 检查结果
if [ $SUCCESS -eq 1 ]; then
    echo "🎉 抢购成功！"
    echo "📸 查看截图：ls -lh /tmp/grab-attempt-*.png"
    echo "📝 查看日志：tail -f $LOG_FILE"
else
    echo "❌ 所有实例都失败了"
    echo "📝 查看日志分析原因：cat $LOG_FILE"
fi

# 清理标记文件
rm -f /tmp/grab-success-instance-*
