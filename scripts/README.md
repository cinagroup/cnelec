# bigmodel.cn GLM-Coding Pro 抢购脚本

## 快速使用

### 1. 配置账号信息

```bash
export BIGMODEL_EMAIL="your@email.com"
export BIGMODEL_PASSWORD="your_password"
export PLAN_TYPE="Pro"  # 或 "Lite"
```

### 2. 立即执行

```bash
cd /root/.openclaw/workspace/cnelec/scripts
python3 grab-pro.py
```

### 3. 定时明天 10 点执行

```bash
cd /root/.openclaw/workspace/cnelec/scripts
bash grab-pro-schedule.sh
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `/tmp/grab-start.png` | 初始页面截图 |
| `/tmp/grab-need-login.png` | 需要登录提示截图 |
| `/tmp/grab-result.png` | 最终结果截图 |
| `/tmp/grab-error.png` | 错误截图（如有） |
| `/tmp/grab-pro-schedule.log` | 定时任务日志 |

## 抢购流程

1. ✅ 访问 https://bigmodel.cn/glm-coding
2. ✅ 检查登录状态
3. ✅ 查找 Pro/Lite 套餐
4. ✅ 点击"即刻订阅"或"特惠订阅"
5. ✅ 选择"连续包季 9 折"选项
6. ✅ 点击"确认购买"或"去支付"
7. ⚠️ **手动完成支付**

## 注意事项

1. **提前登录**：建议先在浏览器手动登录，保持会话
2. **验证码**：如有验证码需要手动处理
3. **支付环节**：脚本只到支付页面，支付需手动完成
4. **网络准备**：确保抢购前网络畅通
5. **提前测试**：建议先运行一次测试熟悉流程

## 故障排除

- 检查网络连接
- 确认账号密码正确
- 查看截图文件了解执行状态
- 可能需要调整选择器（页面结构可能变化）
- 如遇风控，尝试手动购买一次建立信任

## 套餐信息

| 套餐 | 价格 | 说明 |
|------|------|------|
| **Lite** | ￥44/月（连续包季 9 折） | 适合小型 Repo 轻量级迭代 |
| **Pro** | 详情见页面 | 3x Claude Pro 用量额度，支持 20+ 编程工具 |
