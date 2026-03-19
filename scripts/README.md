# bigmodel.cn GLM-Coding Pro 抢购脚本

## 🚀 快速使用

### 方案 A：标准抢购（推荐）

```bash
cd /root/.openclaw/workspace/cnelec/scripts
bash grab-pro-schedule.sh
```

### 方案 B：高并发抢购（热门商品）

```bash
cd /root/.openclaw/workspace/cnelec/scripts
bash grab-pro-concurrent.sh 5  # 5 个实例并发
```

### 方案 C：守护进程模式（最可靠）

```bash
cd /root/.openclaw/workspace/cnelec/scripts
bash grab-pro-guardian.sh
```

---

## 📦 脚本清单

| 文件 | 用途 | 适用场景 |
|------|------|----------|
| `grab-pro.py` | 基础抢购脚本 | 普通抢购 |
| `grab-pro-fast.py` | 快速重试抢购 | 高并发抢购 |
| `grab-pro-concurrent.sh` | 多实例并发抢购 | 极热抢购 |
| `grab-pro-guardian.sh` | 定时守护进程 | 必须抢到 |
| `grab-pro-schedule.sh` | 定时任务启动器 | 标准抢购 |
| `pre-login.py` | 预登录脚本 | 提前准备 |
| `test-grab.sh` | 测试脚本 | 测试用 |
| `GRAB-STRATEGY.md` | 详细策略指南 | 高级配置 |

---

## 输出文件

| 文件 | 说明 |
|------|------|
| `/tmp/grab-start.png` | 初始页面截图 |
| `/tmp/grab-need-login.png` | 需要登录提示截图 |
| `/tmp/grab-result.png` | 最终结果截图 |
| `/tmp/grab-error.png` | 错误截图（如有） |
| `/tmp/grab-pro-schedule.log` | 定时任务日志 |
| `/tmp/grab-concurrent.log` | 并发抢购日志 |
| `/tmp/grab-guardian.log` | 守护进程日志 |

---

## 抢购流程

1. ✅ 访问 https://bigmodel.cn/glm-coding
2. ✅ 检查登录状态
3. ✅ 查找 Pro/Lite 套餐
4. ✅ 点击"即刻订阅"或"特惠订阅"
5. ✅ 选择"连续包季 9 折"选项
6. ✅ 点击"确认购买"或"去支付"
7. ⚠️ **手动完成支付**

---

## 高并发策略

### 为什么需要高并发？

- 📈 **页面被挤爆**：大量用户同时访问，服务器响应变慢
- ⏱️ **时间敏感**：限量商品几秒内售罄
- 🤖 **反爬虫**：单次请求可能失败，需要多次尝试

### 解决方案

1. **多实例并发**：同时运行多个浏览器实例
2. **快速重试**：失败后立即重试，不等待
3. **提前预热**：提前加载页面，保持连接
4. **随机延迟**：避免被识别为机器人

### 配置参数

```bash
# 增加重试次数
export MAX_RETRIES=100

# 减少重试间隔
export RETRY_DELAY=0.2

# 增加并发数
bash grab-pro-concurrent.sh 10
```

---

## 注意事项

1. **提前登录**：建议先在浏览器手动登录，保持会话
2. **验证码**：如有验证码需要手动处理
3. **支付环节**：脚本只到支付页面，支付需手动完成
4. **网络准备**：确保抢购前网络畅通
5. **提前测试**：建议先运行一次测试熟悉流程
6. **资源监控**：高并发会占用较多 CPU 和内存

---

## 故障排除

### 页面加载超时

```bash
export PAGE_TIMEOUT=20000  # 增加到 20 秒
```

### 被识别为机器人

```bash
export ENABLE_RANDOM_DELAY=true  # 启用随机延迟
```

### 内存不足

```bash
bash grab-pro-concurrent.sh 2  # 减少并发数
```

### 登录失败

```bash
# 先手动登录一次
python3 pre-login.py
```

---

## 套餐信息

| 套餐 | 价格 | 说明 |
|------|------|------|
| **Lite** | ￥44/月（连续包季 9 折） | 适合小型 Repo 轻量级迭代 |
| **Pro** | 详情见页面 | 3x Claude Pro 用量额度，支持 20+ 编程工具 |

---

## 详细文档

查看完整的抢购策略指南：

```bash
cat GRAB-STRATEGY.md
```

---

**祝抢购顺利！🎉**
