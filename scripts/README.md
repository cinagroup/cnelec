# bigmodel.cn Pro 抢购脚本

## 快速使用

### 1. 配置账号信息

```bash
export BIGMODEL_EMAIL="your@email.com"
export BIGMODEL_PASSWORD="your_password"
```

### 2. 立即执行

```bash
cd /root/.openclaw/workspace/cnelec/scripts
python3 grab-pro.py
```

### 3. 定时明天 10 点执行

```bash
cd /root/.openclaw/workspace/cnelec/scripts
python3 grab-pro.py --schedule
```

## 输出文件

- `/tmp/grab-start.png` - 初始页面截图
- `/tmp/grab-logged.png` - 登录后截图
- `/tmp/grab-result.png` - 最终结果截图
- `/tmp/grab-error.png` - 错误截图（如有）

## 注意事项

1. **提前测试**：建议先手动登录一次，确保账号正常
2. **保持会话**：如果已登录，脚本会自动检测
3. **验证码**：如有验证码需要手动处理
4. **支付环节**：脚本只到支付页面，支付需手动完成

## 故障排除

- 检查网络连接
- 确认账号密码正确
- 查看截图文件了解执行状态
- 可能需要调整选择器（页面结构可能变化）
