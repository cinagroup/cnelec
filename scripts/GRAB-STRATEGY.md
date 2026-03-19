# 🚀 bigmodel.cn 抢购策略配置指南

## 📊 抢购策略对比

| 脚本 | 适用场景 | 并发数 | 重试次数 | 成功率 |
|------|---------|--------|----------|--------|
| `grab-pro.py` | 普通抢购 | 1 | 10 | ⭐⭐⭐ |
| `grab-pro-fast.py` | 高并发抢购 | 1 | 50 | ⭐⭐⭐⭐ |
| `grab-pro-concurrent.sh` | 极热抢购 | 3-5 | 30×N | ⭐⭐⭐⭐⭐ |
| `grab-pro-guardian.sh` | 定时守护 | 5 | 100×N | ⭐⭐⭐⭐⭐ |

---

## 🎯 推荐方案

### 方案 A：标准抢购（推荐）

适用于：有一定竞争，但不是特别激烈

```bash
cd /root/.openclaw/workspace/cnelec/scripts
bash grab-pro-schedule.sh
```

- ✅ 自动明天 10 点执行
- ✅ 单实例，资源占用少
- ✅ 50 次重试

---

### 方案 B：高并发抢购（推荐用于热门商品）

适用于：非常热门，页面经常被挤爆

```bash
cd /root/.openclaw/workspace/cnelec/scripts
bash grab-pro-concurrent.sh 5
```

- ✅ 5 个实例同时抢购
- ✅ 总共 150 次尝试
- ✅ 成功率极高
- ⚠️ 资源占用较多

---

### 方案 C：守护进程模式（最可靠）

适用于：必须抢到，不惜代价

```bash
cd /root/.openclaw/workspace/cnelec/scripts
bash grab-pro-guardian.sh
```

- ✅ 提前 5 分钟预热
- ✅ 准时 10 点执行
- ✅ 并发 5 实例
- ✅ 失败后自动重试 3 轮
- ✅ 后台运行，可关闭终端

---

## ⚙️ 高级配置

### 环境变量

```bash
# 账号配置
export BIGMODEL_EMAIL="cinagroup"
export BIGMODEL_PASSWORD="qq123456789"
export PLAN_TYPE="Pro"

# 抢购策略配置
export MAX_RETRIES=50           # 最大重试次数（默认 50）
export RETRY_DELAY=0.3          # 重试间隔秒数（默认 0.3）
export PAGE_TIMEOUT=10000       # 页面加载超时毫秒（默认 10000）
export CLICK_TIMEOUT=3000       # 点击超时毫秒（默认 3000）
export ENABLE_RANDOM_DELAY=true # 是否启用随机延迟
```

### 调整并发数

```bash
# 3 个实例（温和）
bash grab-pro-concurrent.sh 3

# 5 个实例（推荐）
bash grab-pro-concurrent.sh 5

# 10 个实例（激进，可能需要更强服务器）
bash grab-pro-concurrent.sh 10
```

---

## 📈 成功率优化技巧

### 1. 提前预热

提前打开页面，保持连接活跃：

```bash
# 提前 5 分钟执行预热
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://bigmodel.cn/glm-coding')
    print('✅ 预热完成')
    browser.close()
"
```

### 2. 网络优化

- 使用有线网络（比 WiFi 稳定）
- 关闭其他占用带宽的应用
- 如果可能，使用 CDN 加速

### 3. 系统资源

确保服务器有足够资源：

```bash
# 检查内存
free -h

# 检查 CPU
top -bn1 | head -5

# 关闭不必要的进程
```

### 4. 时间同步

确保系统时间准确：

```bash
# 同步时间
ntpdate -u pool.ntp.org

# 或使用 systemd-timesyncd
timedatectl status
```

---

## 🧪 测试脚本

在正式抢购前，建议先测试：

```bash
# 立即测试一次
cd /root/.openclaw/workspace/cnelec/scripts
bash test-grab.sh

# 测试并发模式
bash grab-pro-concurrent.sh 2

# 查看测试结果
ls -lh /tmp/grab-*.png
```

---

## 📊 监控抢购进度

### 实时查看日志

```bash
# 查看实时日志
tail -f /tmp/grab-concurrent.log

# 查看守护进程日志
tail -f /tmp/grab-guardian.log

# 搜索成功关键词
grep -i "成功\|success" /tmp/grab-*.log
```

### 检查截图

```bash
# 查看最新截图
ls -lht /tmp/grab-*.png | head -5

# 查看截图内容
display /tmp/grab-attempt-50.png  # 需要 ImageMagick
```

### 检查进程状态

```bash
# 查看抢购进程
ps aux | grep grab-pro

# 查看守护进程
cat /tmp/grab-guardian.pid
```

---

## 🆘 故障排除

### 问题 1：页面加载超时

```bash
# 增加超时时间
export PAGE_TIMEOUT=20000
export CLICK_TIMEOUT=5000
```

### 问题 2：被识别为机器人

```bash
# 启用随机延迟
export ENABLE_RANDOM_DELAY=true

# 增加延迟范围
# 修改脚本中的 random_sleep 参数
```

### 问题 3：内存不足

```bash
# 减少并发数
bash grab-pro-concurrent.sh 2

# 或减少重试次数
export MAX_RETRIES=20
```

### 问题 4：登录失败

```bash
# 先手动登录一次，保存 Cookie
python3 pre-login.py

# 检查账号密码
echo $BIGMODEL_EMAIL
```

---

## 📞 紧急联系

如果抢购过程中遇到问题：

1. 查看日志：`cat /tmp/grab-*.log`
2. 查看截图：`ls /tmp/grab-*.png`
3. 检查进程：`ps aux | grep grab`
4. 重新启动：先 `kill` 旧进程，再重新执行

---

## ✅ 抢购成功后的操作

1. **立即支付**：脚本会停在支付页面，需要手动完成支付
2. **保存凭证**：截图保存订单信息
3. **验证权益**：登录账号检查 Pro 权益是否到账
4. **清理资源**：删除临时文件和进程

```bash
# 清理临时文件
rm -f /tmp/grab-*.png
rm -f /tmp/grab-*.log
rm -f /tmp/bigmodel_cookies.json
```

---

**祝抢购顺利！🎉**
