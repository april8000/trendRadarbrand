# GitHub Actions 自动运行配置指南

本文档详细介绍如何配置 GitHub Actions 实现 TrendRadar 的自动化运行。

## 📋 目录

- [功能特性](#功能特性)
- [前置准备](#前置准备)
- [配置步骤](#配置步骤)
- [Secrets 配置清单](#secrets-配置清单)
- [运行时间配置](#运行时间配置)
- [手动触发](#手动触发)
- [查看运行日志](#查看运行日志)
- [常见问题](#常见问题)

## ✨ 功能特性

GitHub Actions 配置（`.github/workflows/crawler.yml`）提供以下功能：

- ✅ **自动定时运行**：每天北京时间 16:00 自动执行（可自定义）
- ✅ **手动触发**：支持在 GitHub 网页上手动运行
- ✅ **自动推送结果**：支持飞书、钉钉、企业微信、Telegram、邮件等
- ✅ **AI 智能搜索**：当热搜结果不足时自动补充养老资讯
- ✅ **结果自动保存**：运行结果自动提交到仓库

## 📝 前置准备

### 1. Fork 本项目到你的 GitHub 账号

点击项目页面右上角的 "Fork" 按钮。

### 2. 准备配置文件

确保仓库中存在以下文件：

- `config/config.yaml` - 主配置文件
- `config/frequency_words.txt` - 关键词配置文件

如果没有，参考项目文档创建这两个文件并提交到仓库。

### 3. 获取 API 密钥

#### AI 智能搜索（可选）

如需启用 AI 智能搜索功能，需要获取以下 API 密钥：

**Serper API Key**（必需）
1. 访问 https://serper.dev/
2. 使用 Google 账号注册登录
3. 在 Dashboard 中找到 API Key
4. 免费额度：2500 次/月

**Gemini API Key**（可选，推荐）
1. 访问 https://aistudio.google.com/app/apikey
2. 登录 Google 账号
3. 点击 "Create API Key"
4. 免费额度：每分钟 15 次请求

> 💡 **提示**：如果不配置 Gemini API Key，AI 搜索会使用 Serper 搜索结果（仍然有效）。

#### 通知渠道（可选）

根据需要配置以下通知渠道的 API 密钥/Webhook：

- 飞书：获取 Webhook URL
- 钉钉：获取 Webhook URL
- 企业微信：获取 Webhook URL
- Telegram：获取 Bot Token 和 Chat ID
- 邮件：准备 SMTP 服务器信息

## 🔧 配置步骤

### 步骤 1：进入仓库 Secrets 设置

1. 打开你 Fork 的仓库
2. 点击 `Settings`（设置）
3. 左侧菜单点击 `Secrets and variables` → `Actions`
4. 点击 `New repository secret`（新建密钥）

### 步骤 2：添加 Secrets

根据你的需求，添加以下 Secrets：

#### AI 智能搜索（推荐配置）

| Secret Name | 说明 | 必需性 | 示例值 |
|-------------|------|--------|--------|
| `SERPER_API_KEY` | Serper API 密钥 | AI 搜索必需 | `3cab25879262b63b47afd75c9981d7286b453f97` |
| `GEMINI_API_KEY` | Gemini API 密钥 | 可选 | `AIzaSyA0baPd...` |

#### 通知渠道（按需配置）

| Secret Name | 说明 | 示例值 |
|-------------|------|--------|
| `FEISHU_WEBHOOK_URL` | 飞书机器人 Webhook | `https://open.feishu.cn/open-apis/bot/v2/hook/xxx` |
| `DINGTALK_WEBHOOK_URL` | 钉钉机器人 Webhook | `https://oapi.dingtalk.com/robot/send?access_token=xxx` |
| `WEWORK_WEBHOOK_URL` | 企业微信机器人 Webhook | `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx` |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | `123456789` |
| `EMAIL_FROM` | 发件邮箱 | `your-email@gmail.com` |
| `EMAIL_PASSWORD` | 邮箱授权码 | `abcd efgh ijkl mnop` |
| `EMAIL_TO` | 收件邮箱 | `recipient@example.com` |
| `EMAIL_SMTP_SERVER` | SMTP 服务器 | `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | SMTP 端口 | `587` |

### 步骤 3：启用 GitHub Actions

1. 进入仓库的 `Actions` 标签页
2. 如果提示 Actions 未启用，点击 `I understand my workflows, go ahead and enable them`
3. 找到 "Hot News Crawler" workflow
4. 点击 `Enable workflow`

### 步骤 4：配置 config.yaml

在 `config/config.yaml` 中启用 AI 搜索：

```yaml
# AI 智能搜索配置（当热搜筛选结果不足时自动触发）
ai_search:
  enabled: true  # 启用 AI 智能搜索
  trigger_threshold: 3  # 当结果少于此数量时触发
  serper_api_key: ""  # 留空，从环境变量读取
  gemini_api_key: ""  # 留空，从环境变量读取
  search_keywords:  # 搜索关键词
    - "养老保险政策"
    - "养老金调整"
    - "商业养老保险"
    - "个人养老金"
    - "养老服务"
    - "养老改革"
    - "退休金上调"
    - "养老体系"
  time_range_hours: 24  # 搜索过去24小时
  max_results: 15  # 最多返回15条
  gemini_model: "gemini-1.5-flash"
  relevance_threshold: 5  # 相关性评分阈值
```

提交更改到 GitHub：

```bash
git add config/config.yaml
git commit -m "Enable AI search for GitHub Actions"
git push
```

## ⏰ 运行时间配置

默认运行时间：**每天北京时间 16:00**（UTC 8:00）

修改运行时间：编辑 `.github/workflows/crawler.yml` 第 6 行的 cron 表达式：

```yaml
on:
  schedule:
    - cron: "0 8 * * *"  # UTC 时间，北京时间 +8 小时
```

### Cron 表达式示例

| 表达式 | 说明 | 北京时间 |
|--------|------|----------|
| `0 8 * * *` | 每天 1 次 | 16:00 |
| `0 0,12 * * *` | 每天 2 次 | 08:00, 20:00 |
| `0 0,6,12,18 * * *` | 每天 4 次 | 08:00, 14:00, 20:00, 02:00 |
| `0 * * * *` | 每小时 1 次 | 每小时整点 |
| `*/30 * * * *` | 每 30 分钟 | 每半小时 |
| `0 0-14 * * *` | 每天 8:00-22:00，每小时 1 次 | 工作时间段 |

**注意**：
- GitHub Actions 使用 UTC 时间，需要减 8 小时
- 北京时间 16:00 = UTC 08:00
- 实际运行时间可能有 5-15 分钟延迟

### 推荐配置

根据使用场景选择：

- **养老资讯监控**：`0 0,8 * * *`（每天 2 次：8:00, 16:00）
- **实时监控**：`*/30 * * * *`（每 30 分钟）
- **节省资源**：`0 8 * * *`（每天 1 次）

## 🚀 手动触发

除了定时自动运行，你也可以手动触发：

1. 进入仓库的 `Actions` 标签页
2. 点击左侧的 "Hot News Crawler"
3. 点击右上角的 `Run workflow` 按钮
4. 选择分支（通常是 `main` 或 `master`）
5. 点击 `Run workflow` 确认

## 📊 查看运行日志

### 查看运行状态

1. 进入 `Actions` 标签页
2. 查看最近的运行记录
3. 点击某次运行查看详细日志

### 查看运行结果

运行结果会自动提交到仓库：

- HTML 报告：`output/YYYY年MM月DD日/html/`
- 文本记录：`output/YYYY年MM月DD日/txt/`

访问这些文件即可查看爬取结果。

## 🔍 Secrets 配置清单

### 最小配置（仅热搜，无通知）

```
无需配置任何 Secrets
```

### 推荐配置（热搜 + AI 搜索 + 通知）

```
✅ SERPER_API_KEY
✅ GEMINI_API_KEY
✅ 至少一个通知渠道（飞书/钉钉/企业微信/Telegram/邮件）
```

### 完整配置（所有功能）

```
✅ SERPER_API_KEY
✅ GEMINI_API_KEY
✅ FEISHU_WEBHOOK_URL
✅ DINGTALK_WEBHOOK_URL
✅ WEWORK_WEBHOOK_URL
✅ TELEGRAM_BOT_TOKEN
✅ TELEGRAM_CHAT_ID
✅ EMAIL_FROM
✅ EMAIL_PASSWORD
✅ EMAIL_TO
✅ EMAIL_SMTP_SERVER
✅ EMAIL_SMTP_PORT
```

## ❓ 常见问题

### Q1: Actions 运行失败，提示 "config/config.yaml 文件不存在"

**A:** 确保你的仓库中存在 `config/config.yaml` 文件。如果没有：

1. 从项目根目录复制 `config/config.yaml.example`（如果有）
2. 或者创建一个新的 `config/config.yaml` 参考项目文档
3. 提交并推送到 GitHub

### Q2: AI 搜索功能没有生效

**A:** 检查以下几点：

1. 确认在 GitHub Secrets 中添加了 `SERPER_API_KEY`
2. 确认 `config/config.yaml` 中 `ai_search.enabled` 为 `true`
3. 确认热搜结果少于 `trigger_threshold`（默认 3 条）才会触发 AI 搜索

### Q3: Gemini API 调用超时

**A:** 这是正常现象（GitHub Actions 服务器访问 Google 受限）。系统会自动降级：

- 使用 Serper 搜索结果（仍然有效）
- 不影响核心功能
- 如果需要 Gemini 筛选，考虑本地运行或使用国内服务器

### Q4: 如何查看 AI 搜索是否触发了？

**A:** 查看 Actions 运行日志，搜索以下关键词：

```
[警告] 热搜筛选结果仅 X 条，少于阈值 Y 条
[AI] 触发 AI 智能搜索补充养老资讯...
```

### Q5: Actions 运行频率有限制吗？

**A:** GitHub Actions 免费额度：

- **公开仓库**：无限制
- **私有仓库**：每月 2000 分钟

每次运行约 1-3 分钟，按需调整运行频率。

### Q6: 如何暂停自动运行？

**A:** 两种方式：

**方式 1：禁用 Workflow**
1. 进入 `Actions` 标签页
2. 点击 "Hot News Crawler"
3. 点击右上角的 `...` → `Disable workflow`

**方式 2：删除 schedule（保留手动触发）**
编辑 `.github/workflows/crawler.yml`，注释掉 schedule 部分：

```yaml
on:
  # schedule:
  #   - cron: "0 8 * * *"
  workflow_dispatch:  # 保留手动触发
```

### Q7: 通知没有收到

**A:** 检查步骤：

1. 确认在 GitHub Secrets 中正确配置了相应的 Secret
2. 确认 `config/config.yaml` 中启用了对应的通知渠道
3. 查看 Actions 日志，搜索 "发送" 或 "通知" 相关的错误信息
4. 测试 Webhook URL 或邮箱配置是否正确

### Q8: 如何更新 API 密钥？

**A:** 

1. 进入 `Settings` → `Secrets and variables` → `Actions`
2. 找到要更新的 Secret（如 `SERPER_API_KEY`）
3. 点击右侧的 `Update` 按钮
4. 输入新的密钥值
5. 点击 `Update secret` 保存

## 📚 相关文档

- [AI 搜索功能详细说明](AI_SEARCH_README.md)
- [AI 搜索快速开始](AI_SEARCH_QUICKSTART.md)
- [项目主文档](readme.md)

## 🎯 总结

配置 GitHub Actions 自动运行只需 3 步：

1. **添加 Secrets**：在仓库设置中添加 API 密钥
2. **配置文件**：确保 `config.yaml` 正确配置
3. **启用 Actions**：在 Actions 页面启用 workflow

之后系统会自动定时运行，你也可以随时手动触发！

---

需要帮助？请提交 [Issue](../../issues) 或查看[项目文档](readme.md)。



