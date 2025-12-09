# 📤 TrendRadar AI 增强版 - 分享与使用指南

## 🎯 项目简介

这是 TrendRadar 的 AI 增强版本，新增了**智能养老资讯搜索功能**：

### ✨ 新增功能

- 🔍 **AI 智能搜索**：当现有平台筛选结果不足时，自动使用 Serper API + Gemini AI 搜索养老相关资讯
- 🎯 **精准过滤**：AI 评分筛选，只保留高相关度的养老保险、政策、服务等资讯
- ⚙️ **灵活配置**：可自定义触发阈值、搜索关键词、时间范围等
- 🌍 **完善的国际化支持**：修复了 Windows 下的编码问题
- 🔧 **代理问题修复**：解决了网络代理导致的连接失败问题

---

## 🚀 快速开始

### 方式一：直接使用（推荐新手）

1. **访问仓库**：https://github.com/april8000/TrendRadar

2. **下载代码**：
   - 点击绿色的 `Code` 按钮
   - 选择 `Download ZIP`
   - 解压到本地

3. **安装依赖**：
   ```bash
   cd TrendRadar-master
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

4. **配置 API 密钥**：
   - 编辑 `config/config.yaml`
   - 填写 `serper_api_key` 和 `gemini_api_key`
   - 或者设置环境变量（推荐）：
     ```bash
     # Windows PowerShell
     $env:SERPER_API_KEY="your_serper_key"
     $env:GEMINI_API_KEY="your_gemini_key"
     
     # Linux/Mac
     export SERPER_API_KEY="your_serper_key"
     export GEMINI_API_KEY="your_gemini_key"
     ```

5. **运行**：
   ```bash
   python main.py
   ```

### 方式二：Git Clone（推荐开发者）

```bash
git clone https://github.com/april8000/TrendRadar.git
cd TrendRadar
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 配置环境变量
python main.py
```

### 方式三：GitHub Actions 自动化

Fork 本仓库后：

1. **添加 Secrets**：
   - 进入 `Settings` → `Secrets and variables` → `Actions`
   - 添加 `SERPER_API_KEY` 和 `GEMINI_API_KEY`

2. **启用 Actions**：
   - 进入 `Actions` 标签页
   - 点击 `Enable workflows`

3. **自动运行**：
   - 每天 8:00 和 20:00 自动执行
   - 或手动点击 `Run workflow` 触发

4. **查看结果**：
   - 在 Actions 运行记录中下载 `crawler-results` 压缩包
   - 解压查看 HTML/TXT 报告

---

## 🔑 获取 API 密钥

### Serper API（Google 搜索）

1. 访问：https://serper.dev
2. 注册账号（免费 2500 次搜索/月）
3. 复制 API Key

### Gemini API（AI 过滤）

1. 访问：https://aistudio.google.com/apikey
2. 登录 Google 账号
3. 创建 API Key（免费）

---

## ⚙️ 配置说明

编辑 `config/config.yaml` 中的 `ai_search` 部分：

```yaml
ai_search:
  enabled: true                      # 是否启用 AI 搜索
  trigger_threshold: 3               # 结果少于此数量时触发
  search_keywords:                   # 自定义搜索关键词
    - "养老保险政策"
    - "养老金调整"
    - "个人养老金"
  time_range_hours: 24               # 搜索过去 N 小时的新闻
  max_results: 15                    # 每次搜索最大结果数
  relevance_threshold: 5             # AI 评分阈值（0-10）
```

---

## 📚 详细文档

- [AI 搜索功能详解](AI_SEARCH_README.md)
- [AI 搜索快速入门](AI_SEARCH_QUICKSTART.md)
- [GitHub Actions 配置指南](GITHUB_ACTIONS_GUIDE.md)
- [部署总结](DEPLOYMENT_SUMMARY.md)

---

## 🐛 常见问题

### Q1: 提示 "ProxyError" 错误
**A**: 清除系统代理设置：
```powershell
# Windows
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""

# 或修改代码（已在此版本中修复）
```

### Q2: 提示 "UnicodeEncodeError" 错误
**A**: 此版本已修复 Windows 终端编码问题，所有 emoji 已替换为文本标签。

### Q3: Serper API 返回 429 错误
**A**: API 调用频率超限，等待 1 分钟后重试，或升级 Serper 套餐。

### Q4: Gemini API 无法访问
**A**: 
- 确认 API Key 正确
- 检查网络连接（可能需要代理）
- 查看 https://status.cloud.google.com/ 服务状态

### Q5: 想修改搜索主题（不是养老）
**A**: 编辑 `config/config.yaml` 的 `search_keywords` 部分，替换为您关注的关键词。

---

## 🤝 贡献与反馈

- **Issue**：https://github.com/april8000/TrendRadar/issues
- **Pull Request**：欢迎提交改进
- **讨论**：https://github.com/april8000/TrendRadar/discussions

---

## 📄 开源协议

本项目基于 GPL-3.0 协议开源。

---

## 🙏 致谢

- 原项目：[sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)
- Serper API：https://serper.dev
- Google Gemini：https://ai.google.dev

---

## 📧 联系方式

如有任何问题或建议，欢迎：
- 提 Issue：https://github.com/april8000/TrendRadar/issues
- 发起讨论：https://github.com/april8000/TrendRadar/discussions

---

**祝使用愉快！如果觉得有用，请给个 ⭐ Star 支持一下！**


