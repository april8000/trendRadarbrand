# GitHub Actions 配置检查清单 ✅

快速配置 GitHub Actions 自动运行的完整检查清单。

## 📋 配置前检查

- [ ] 已将项目 Fork 到自己的 GitHub 账号
- [ ] 仓库中存在 `config/config.yaml` 文件
- [ ] 仓库中存在 `config/frequency_words.txt` 文件

## 🔑 API 密钥准备（AI 搜索）

### Serper API（必需）

- [ ] 访问 https://serper.dev/ 注册
- [ ] 获取 API Key
- [ ] 复制保存 API Key

### Gemini API（可选，推荐）

- [ ] 访问 https://aistudio.google.com/app/apikey
- [ ] 创建 API Key
- [ ] 复制保存 API Key

## 🔧 GitHub Secrets 配置

进入仓库 `Settings` → `Secrets and variables` → `Actions`

### AI 智能搜索（推荐）

- [ ] 添加 Secret: `SERPER_API_KEY`
- [ ] 添加 Secret: `GEMINI_API_KEY`（可选）

### 通知渠道（按需选择至少一个）

- [ ] **飞书**：添加 `FEISHU_WEBHOOK_URL`
- [ ] **钉钉**：添加 `DINGTALK_WEBHOOK_URL`
- [ ] **企业微信**：添加 `WEWORK_WEBHOOK_URL`
- [ ] **Telegram**：添加 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`
- [ ] **邮件**：添加 `EMAIL_FROM`, `EMAIL_PASSWORD`, `EMAIL_TO`, `EMAIL_SMTP_SERVER`, `EMAIL_SMTP_PORT`

## ⚙️ 配置文件修改

编辑 `config/config.yaml`：

```yaml
# AI 智能搜索配置
ai_search:
  enabled: true  # ✅ 改为 true
  trigger_threshold: 3
  serper_api_key: ""  # ✅ 留空（从环境变量读取）
  gemini_api_key: ""  # ✅ 留空（从环境变量读取）
  search_keywords:
    - "养老保险政策"
    - "养老金调整"
    - "商业养老保险"
    - "个人养老金"
    - "养老服务"
    # ... 其他关键词
```

- [ ] 设置 `ai_search.enabled: true`
- [ ] API Key 字段留空（让其从环境变量读取）
- [ ] 根据需要调整搜索关键词
- [ ] 提交更改到 GitHub：
  ```bash
  git add config/config.yaml
  git commit -m "Enable AI search"
  git push
  ```

## 🚀 启用 GitHub Actions

- [ ] 进入仓库的 `Actions` 标签页
- [ ] 点击 `I understand my workflows, go ahead and enable them`
- [ ] 找到 "Hot News Crawler" workflow
- [ ] 点击 `Enable workflow`

## 🧪 测试运行

### 方法 1：手动触发测试

- [ ] 进入 `Actions` 标签页
- [ ] 点击 "Hot News Crawler"
- [ ] 点击 `Run workflow` 按钮
- [ ] 选择分支并确认运行
- [ ] 等待运行完成（1-3 分钟）
- [ ] 查看日志确认无错误

### 方法 2：等待自动运行

- [ ] 默认每天北京时间 16:00 自动运行
- [ ] 第二天查看运行结果

## ✅ 验证成功

运行成功的标志：

- [ ] Actions 页面显示绿色的 ✓
- [ ] 日志中显示 "获取 xxx 成功（最新数据）"
- [ ] 仓库中出现 `output/` 目录和结果文件
- [ ] 收到通知推送（如果配置了通知渠道）

### 验证 AI 搜索功能

在日志中搜索以下内容：

- [ ] 看到 "[警告] 热搜筛选结果仅 X 条" → AI 搜索已触发
- [ ] 看到 "[AI] 智能搜索启动" → AI 搜索正在运行
- [ ] 看到 "[完成] AI 搜索完成" → AI 搜索成功

## ⚠️ 常见问题快速修复

### ❌ 配置文件不存在

```bash
# 确保文件存在
ls -la config/config.yaml
ls -la config/frequency_words.txt

# 如果不存在，创建并提交
git add config/
git commit -m "Add config files"
git push
```

### ❌ API Key 无效

- [ ] 检查 Secrets 中的 API Key 是否正确（无多余空格）
- [ ] 确认 API Key 未过期
- [ ] 在 API 提供商网站验证 API Key 状态

### ❌ Actions 运行失败

- [ ] 查看完整日志找到错误信息
- [ ] 检查是否有权限问题（确保 Actions 已启用）
- [ ] 验证所有必需的 Secrets 都已配置

### ❌ 没有收到通知

- [ ] 确认通知渠道的 Secret 配置正确
- [ ] 检查 `config.yaml` 中对应通知渠道已启用
- [ ] 测试 Webhook URL 或邮箱配置

## 🎯 配置完成！

全部完成后，你的 TrendRadar 将：

✅ 每天自动运行（默认 16:00）
✅ 自动抓取 11 个平台的热搜
✅ 当热搜结果不足时，自动 AI 搜索补充养老资讯
✅ 自动推送结果到你配置的通知渠道
✅ 结果自动保存到仓库

## 📚 详细文档

- [GitHub Actions 完整配置指南](GITHUB_ACTIONS_GUIDE.md)
- [AI 搜索功能说明](AI_SEARCH_README.md)
- [项目主文档](readme.md)

---

遇到问题？提交 [Issue](../../issues) 寻求帮助。



