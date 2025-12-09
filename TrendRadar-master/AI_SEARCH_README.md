# AI 智能搜索功能使用指南

## 功能简介

当热搜榜单筛选的养老资讯不足时（默认少于 3 条），系统会自动调用 Serper API 搜索最近 24 小时的养老相关新闻，并使用 Google Gemini AI 进行智能筛选，确保获取高质量的养老保险和政策资讯。

## 核心特性

- ✅ **自动触发**：热搜结果不足时自动启动
- ✅ **智能筛选**：Gemini AI 评分过滤低质量内容
- ✅ **时效性强**：搜索过去 24 小时的最新资讯
- ✅ **完全免费**：使用 API 免费额度，零成本运行
- ✅ **无缝集成**：结果自动合并到推送消息中

## 配置步骤

### 1. 获取 API Keys

#### Serper API Key

1. 访问：https://serper.dev/
2. 注册账号并验证邮箱
3. 登录后访问：https://serper.dev/api-key
4. 复制 API Key（格式：一串字母数字组合）
5. **免费额度**：2500 次/月

#### Gemini API Key

1. 访问：https://aistudio.google.com/
2. 登录 Google 账号
3. 点击 "Get API Key" 或访问：https://aistudio.google.com/app/apikey
4. 创建新的 API Key
5. 复制 API Key（格式：AIza 开头的字符串）
6. **免费额度**：每天 1500 次请求

**重要提醒**：
- ⚠️ 请妥善保管 API Keys，不要公开分享
- 🔒 建议通过环境变量配置，而非写在配置文件中

### 2. 配置方式

有两种配置方式，推荐使用**方式一**（更安全）：

#### 方式一：环境变量配置（推荐）

**GitHub Actions 部署：**

在你 Fork 后的仓库中，进入 `Settings` > `Secrets and variables` > `Actions` > `New repository secret`：

```
名称：SERPER_API_KEY
值：你的 Serper API Key

名称：GEMINI_API_KEY
值：你的 Gemini API Key
```

**Docker 部署：**

在 `.env` 文件或 `docker-compose.yml` 中添加：

```bash
SERPER_API_KEY=你的_Serper_API_Key
GEMINI_API_KEY=你的_Gemini_API_Key
```

**本地运行：**

```bash
# Windows (PowerShell)
$env:SERPER_API_KEY="你的_Serper_API_Key"
$env:GEMINI_API_KEY="你的_Gemini_API_Key"

# Linux/Mac
export SERPER_API_KEY="你的_Serper_API_Key"
export GEMINI_API_KEY="你的_Gemini_API_Key"
```

#### 方式二：配置文件（不推荐，仅用于测试）

编辑 `config/config.yaml`，找到 `ai_search` 配置节：

```yaml
ai_search:
  enabled: true
  serper_api_key: "你的_Serper_API_Key"  # 在此填写
  gemini_api_key: "你的_Gemini_API_Key"  # 在此填写
```

**⚠️ 警告**：如果使用 GitHub 部署，请勿在配置文件中填写 API Keys，否则会被公开！

### 3. 调整配置（可选）

在 `config/config.yaml` 中可以调整以下参数：

```yaml
ai_search:
  enabled: true  # 是否启用 AI 搜索
  trigger_threshold: 3  # 触发阈值：当热搜结果少于此数量时触发
  search_keywords:  # 搜索关键词（根据需求调整）
    - "养老保险政策"
    - "养老金调整"
    - "商业养老保险"
    - "个人养老金"
    - "养老服务"
    - "养老改革"
    - "退休金上调"
    - "养老体系"
  time_range_hours: 24  # 搜索时间范围（小时）
  max_results: 15  # 每次搜索的最大结果数
  gemini_model: "gemini-1.5-flash"  # Gemini 模型
  relevance_threshold: 5  # 相关性阈值（0-10分，保留>=此分数的新闻）
```

### 4. 安装依赖

```bash
# 方式一：使用 pip
pip install -r requirements.txt

# 方式二：如果之前已安装，只安装新依赖
pip install google-generativeai>=0.8.0
```

## 使用说明

### 自动运行

配置完成后，系统会在以下情况自动触发 AI 搜索：

1. 运行正常的热搜抓取和筛选流程
2. 如果筛选结果 < 3 条（可配置），自动触发 AI 搜索
3. AI 搜索的结果会自动合并到最终报告中

### 推送消息格式

AI 搜索的结果会特别标记，便于识别：

```
📊 热点词汇统计

🔥 [1/2] 养老保险 养老金 : 8 条

  1. [知乎] 个人养老金制度改革 [**2**] - 10时30分 (2次)
  
  2. [AI智能搜索] 🤖 人社部发布养老保险新政策 - 09时15分
  
  3. [AI智能搜索] 🤖 2025年养老金上调最新方案公布 - 11时20分
  
  4. [微博] 养老金上调方案公布 [**5**] - 11时00分 (1次)

━━━━━━━━━━━━━━━━━━━

🆕 本次新增热点新闻 (共 3 条)

**AI智能搜索** (2 条):
  1. 人社部发布养老保险新政策
  2. 2025年养老金上调最新方案公布

**知乎** (1 条):
  1. 个人养老金制度改革 [**2**]
```

**标识说明：**
- 🤖 图标：表示来自 AI 智能搜索
- 来源显示："AI智能搜索" 而非具体平台
- 无排名信息：AI 搜索结果没有热搜排名

## 工作流程

```
┌─────────────────┐
│  1. 热搜抓取     │
│  (11个平台)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. 关键词筛选   │
│  (frequency_    │
│   words.txt)    │
└────────┬────────┘
         │
         ▼
    ┌───────────┐
    │ 结果>=3条? │
    └─┬─────┬───┘
      │是   │否
      │     │
      │     ▼
      │  ┌──────────────┐
      │  │ 3. AI 搜索    │
      │  │ (Serper API) │
      │  └───────┬──────┘
      │          │
      │          ▼
      │  ┌──────────────┐
      │  │ 4. AI 筛选    │
      │  │ (Gemini AI)  │
      │  └───────┬──────┘
      │          │
      │          ▼
      │  ┌──────────────┐
      │  │ 5. 合并结果   │
      │  └───────┬──────┘
      │          │
      └──────────┘
             │
             ▼
    ┌─────────────────┐
    │  6. 生成报告     │
    │  7. 推送通知     │
    └─────────────────┘
```

## 测试方法

### 测试 AI 搜索功能

创建测试脚本 `test_ai_search.py`：

```python
# coding=utf-8

import os
import sys

# 设置 API Keys（测试用）
os.environ["SERPER_API_KEY"] = "你的_Serper_API_Key"
os.environ["GEMINI_API_KEY"] = "你的_Gemini_API_Key"

# 导入模块
from main import load_config
from ai_search import search_pension_news_with_ai

# 加载配置
config = load_config()

# 测试搜索
print("开始测试 AI 搜索功能...\n")
results = search_pension_news_with_ai(config)

print(f"\n搜索完成，共获取 {len(results)} 条结果：")
for idx, item in enumerate(results[:5], 1):
    print(f"{idx}. {item['title']}")
    print(f"   来源：{item.get('original_source', '未知')}")
    print(f"   链接：{item['url'][:80]}...")
    print()
```

运行测试：

```bash
python test_ai_search.py
```

### 查看运行日志

运行主程序时，会输出详细的 AI 搜索日志：

```
⚠️ 热搜筛选结果仅 1 条，少于阈值 3 条
🤖 触发 AI 智能搜索补充养老资讯...

============================================================
🤖 AI 智能搜索启动
============================================================
🔍 正在搜索: 养老保险政策 OR 养老金调整 OR 商业养老保险 OR ...
   搜索范围: 过去 24 小时
✅ Serper 搜索到 12 条结果
🤖 正在调用 Gemini gemini-1.5-flash 进行智能筛选...
   ✅ Gemini 分析完成，保留 8/12 条
      • ID 0 (评分: 9/10): 关于个人养老金政策调整的权威报道
      • ID 2 (评分: 8/10): 养老保险缴费基数上调相关政策
      • ID 5 (评分: 8/10): 2025年退休金上调方案详解
      ... 还有 5 条
✅ Gemini 筛选后保留 8 条高质量新闻
============================================================
🎉 AI 搜索完成，共获取 8 条养老资讯
============================================================

✅ AI 搜索补充了 8 条养老资讯
```

## 常见问题

### Q1: 如何知道 AI 搜索是否被触发？

**A:** 查看运行日志，如果看到以下信息说明已触发：
```
⚠️ 热搜筛选结果仅 X 条，少于阈值 3 条
🤖 触发 AI 智能搜索补充养老资讯...
```

### Q2: API 调用失败怎么办？

**A:** 系统有自动降级机制：
- Serper 或 Gemini 调用失败时，会自动重试 3 次
- 如果全部失败，会跳过 AI 搜索，使用热搜筛选结果
- 不会影响正常流程

### Q3: 如何调整触发频率？

**A:** 修改 `config/config.yaml` 中的 `trigger_threshold`：
- 设置为 `1`：几乎每次都触发（API 消耗多）
- 设置为 `3`：平衡选择（推荐）
- 设置为 `5`：很少触发（节省 API 额度）

### Q4: 如何查看 API 使用量？

**A:** 
- **Serper**：登录 https://serper.dev/ 查看 Dashboard
- **Gemini**：访问 https://aistudio.google.com/ 查看配额

### Q5: 免费额度够用吗？

**A:** 完全够用！
- 假设每天运行 24 次（每小时一次）
- 触发 AI 搜索约 5-10 次/天
- 每月约 150-300 次搜索
- 远低于 Serper 2500次/月 和 Gemini 45000次/月 的免费额度

### Q6: 如何禁用 AI 搜索？

**A:** 在 `config/config.yaml` 中设置：
```yaml
ai_search:
  enabled: false  # 禁用
```

### Q7: 搜索结果质量不满意？

**A:** 可以调整以下参数：
1. **搜索关键词**：修改 `search_keywords`，增加或删除关键词
2. **相关性阈值**：提高 `relevance_threshold`（如改为 7）只保留高分新闻
3. **时间范围**：缩短 `time_range_hours`（如改为 12）只看最近半天

### Q8: Gemini 评分标准是什么？

**A:** Gemini 会根据以下因素评分（0-10分）：
- **8-10分**：高度相关，政策性强或信息价值高（必须保留）
- **5-7分**：中度相关，有一定参考价值（可以保留）
- **0-4分**：低相关或无关（过滤掉）

默认保留 ≥5 分的新闻。

## 技术细节

### API 限流保护

- **Serper**：每秒最多 1 次请求
- **Gemini**：每分钟最多 15 次请求
- 触发限流时自动等待并重试（指数退避）

### 错误处理

```python
try:
    # AI 搜索
except Exception as e:
    print(f"❌ AI 搜索失败: {e}")
    # 降级：返回热搜筛选结果
    return original_results
```

### 数据格式

AI 搜索结果会转换为与热搜数据一致的格式：

```python
{
    "title": "新闻标题",
    "url": "https://...",
    "mobileUrl": "https://...",
    "source": "AI智能搜索",
    "platform_id": "ai_search",
    "rank": 0,
    "ranks": [],
    "source_type": "ai_search",
    "original_source": "原始来源网站",
    "date": "2 hours ago",
    "snippet": "新闻摘要..."
}
```

## 成本估算

### 免费方案（推荐）

- **Serper API**：2500次/月免费
- **Gemini API**：45000次/月免费
- **预估消耗**：
  - 每天运行 24 次
  - 触发 AI 搜索 5-10 次/天
  - 每月约 150-300 次搜索
- **结论**：完全免费，无需付费！

### 付费方案（如超出免费额度）

- **Serper API**：$50/5000次（约 $0.01/次）
- **Gemini API**：免费额度足够（超出可换其他模型）
- **预估月成本**：$0-5（极少情况）

## 更新日志

### v1.0.0 (2025-11-17)

- ✅ 初始版本发布
- ✅ 支持 Serper API 搜索
- ✅ 支持 Gemini AI 智能筛选
- ✅ 自动触发机制
- ✅ 结果合并和展示
- ✅ 完整的错误处理和降级策略

## 支持与反馈

如有问题或建议，请：
1. 查看主项目 README 中的常见问题
2. 在 GitHub Issues 中提问
3. 提供详细的错误日志和配置信息

---

**祝您使用愉快！** 🎉

