#!/bin/bash
# 抢购脚本测试 - 立即运行一次测试

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧪 bigmodel.cn GLM-Coding Pro 抢购测试"
echo "========================================"
echo ""

# 检查环境变量
if [ -z "$BIGMODEL_EMAIL" ] || [ -z "$BIGMODEL_PASSWORD" ]; then
    echo "⚠️  未配置账号信息，请先设置："
    echo "   export BIGMODEL_EMAIL='your@email.com'"
    echo "   export BIGMODEL_PASSWORD='your_password'"
    echo ""
    echo "💡 或者编辑 ~/.bashrc 添加永久配置"
    echo ""
fi

echo "📄 目标页面：https://bigmodel.cn/glm-coding"
echo "📦 套餐类型：${PLAN_TYPE:-Pro}"
echo ""
echo "🚀 开始测试..."
echo ""

cd "$SCRIPT_DIR"
python3 grab-pro.py

echo ""
echo "========================================"
echo "✅ 测试完成"
echo "📸 查看截图：ls -lh /tmp/grab-*.png"
