# coding=utf-8

"""
AI 智能搜索模块
当热搜筛选结果不足时，自动搜索养老相关资讯并使用 AI 筛选
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests

# 清除代理环境变量，避免代理问题
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AISearchManager:
    """AI 智能搜索管理器"""
    
    def __init__(self, config: Dict):
        """
        初始化 AI 搜索管理器
        
        Args:
            config: 配置字典，包含 AI_SEARCH 配置项
        """
        self.config = config
        self.ai_config = config.get("AI_SEARCH", {})
        
        # API Keys
        self.serper_api_key = self.ai_config.get("SERPER_API_KEY", "")
        self.gemini_api_key = self.ai_config.get("GEMINI_API_KEY", "")
        
        # 搜索配置
        self.search_keywords = self.ai_config.get("SEARCH_KEYWORDS", [])
        self.time_range_hours = self.ai_config.get("TIME_RANGE_HOURS", 24)
        self.max_results = self.ai_config.get("MAX_RESULTS", 15)
        self.relevance_threshold = self.ai_config.get("RELEVANCE_THRESHOLD", 5)
        
        # Gemini 配置
        self.gemini_model_name = self.ai_config.get("GEMINI_MODEL", "gemini-1.5-flash")
        
        # 验证配置
        self._validate_config()
    
    def _validate_config(self):
        """验证配置是否完整"""
        if not self.serper_api_key:
            raise ValueError("未配置 SERPER_API_KEY，请在环境变量或配置文件中设置")
        
        if not self.gemini_api_key:
            raise ValueError("未配置 GEMINI_API_KEY，请在环境变量或配置文件中设置")
        
        if not GEMINI_AVAILABLE:
            raise ImportError("未安装 google-generativeai，请运行: pip install google-generativeai")
        
        if not self.search_keywords:
            raise ValueError("未配置搜索关键词 SEARCH_KEYWORDS")
    
    def search_and_filter(self) -> List[Dict]:
        """
        执行搜索并筛选流程
        
        Returns:
            筛选后的新闻列表
        """
        try:
            print("\n" + "="*60)
            print("[AI] 智能搜索启动")
            print("="*60)
            
            # 1. 使用 Serper API 搜索
            search_results = self._search_with_serper()
            
            if not search_results:
                print("[警告] Serper 搜索未返回结果")
                return []
            
            print(f"[成功] Serper 搜索到 {len(search_results)} 条结果")
            
            # 2. 使用 Gemini 筛选
            filtered_results = self._filter_with_gemini(search_results)
            
            print(f"[成功] Gemini 筛选后保留 {len(filtered_results)} 条高质量新闻")
            
            # 3. 格式化为统一格式
            formatted_results = self._format_results(filtered_results)
            
            print("="*60)
            print(f"[完成] AI 搜索完成，共获取 {len(formatted_results)} 条养老资讯")
            print("="*60 + "\n")
            
            return formatted_results
            
        except Exception as e:
            print(f"[错误] AI 搜索出错: {e}")
            return []
    
    def _search_with_serper(self) -> List[Dict]:
        """
        使用 Serper API 搜索新闻
        
        Returns:
            搜索结果列表
        """
        try:
            # 构建搜索查询
            query = " OR ".join(self.search_keywords)
            
            # API 请求参数
            url = "https://google.serper.dev/news"
            headers = {
                "X-API-KEY": self.serper_api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "num": self.max_results,
                "gl": "cn",  # 地区：中国
                "hl": "zh-cn",  # 语言：中文
                "tbs": f"qdr:d"  # 时间：过去一天
            }
            
            print(f"[搜索] 正在搜索: {query}")
            print(f"   搜索范围: 过去 {self.time_range_hours} 小时")
            
            # 发送请求（添加重试机制）
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 创建 session 并禁用代理
                    session = requests.Session()
                    session.trust_env = False  # 禁用环境变量代理
                    
                    response = session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        news_results = data.get("news", [])
                        
                        # 过滤时间范围
                        filtered_news = self._filter_by_time(news_results)
                        return filtered_news
                    
                    elif response.status_code == 429:
                        # 速率限制，等待后重试
                        wait_time = 2 ** attempt
                        print(f"   [警告] 触发速率限制，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                        continue
                    
                    else:
                        print(f"   [错误] Serper API 错误: {response.status_code}")
                        print(f"   响应内容: {response.text}")
                        return []
                
                except requests.Timeout:
                    if attempt < max_retries - 1:
                        print(f"   [警告] 请求超时，重试 ({attempt + 1}/{max_retries})...")
                        time.sleep(1)
                        continue
                    else:
                        print("   [错误] 请求超时，已达到最大重试次数")
                        return []
            
            return []
            
        except Exception as e:
            print(f"[错误] Serper 搜索失败: {e}")
            return []
    
    def _filter_by_time(self, news_list: List[Dict]) -> List[Dict]:
        """
        按时间范围过滤新闻
        
        Args:
            news_list: 新闻列表
            
        Returns:
            过滤后的新闻列表
        """
        cutoff_time = datetime.now() - timedelta(hours=self.time_range_hours)
        filtered = []
        
        for news in news_list:
            try:
                # Serper 返回的时间格式：相对时间（如 "2 hours ago"）或日期
                date_str = news.get("date", "")
                
                # 简单处理：如果包含 "ago"，说明是最近的新闻
                if "ago" in date_str.lower() or "小时" in date_str or "分钟" in date_str:
                    filtered.append(news)
                # 如果是今天的新闻
                elif "today" in date_str.lower() or "今天" in date_str:
                    filtered.append(news)
                # 其他情况也保留（Serper 已经按时间筛选过了）
                else:
                    filtered.append(news)
            except Exception:
                # 解析失败也保留
                filtered.append(news)
        
        return filtered
    
    def _filter_with_gemini(self, news_list: List[Dict]) -> List[Dict]:
        """
        使用 Gemini AI 筛选和分析新闻
        
        Args:
            news_list: 搜索结果列表
            
        Returns:
            筛选后的高质量新闻列表
        """
        try:
            # 配置 Gemini
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel(self.gemini_model_name)
            
            # 构建新闻摘要供 AI 分析
            news_summaries = []
            for idx, news in enumerate(news_list):
                summary = {
                    "id": idx,
                    "title": news.get("title", ""),
                    "snippet": news.get("snippet", ""),
                    "source": news.get("source", "")
                }
                news_summaries.append(summary)
            
            # 构建 Prompt
            prompt = f"""你是一个养老资讯分析专家。请分析以下新闻列表，筛选出与养老相关的高质量内容。

**重点关注：**
1. 养老保险政策（社保、商业养老保险、个人养老金）
2. 养老金调整和改革
3. 退休相关政策
4. 养老服务和产业
5. 老龄化相关政策

**评分标准（0-10分）：**
- 8-10分：高度相关，政策性强或信息价值高，必须保留
- 5-7分：中度相关，有一定参考价值，可以保留
- 0-4分：低相关或无关，过滤掉

**新闻列表：**
{json.dumps(news_summaries, ensure_ascii=False, indent=2)}

**要求：**
请对每条新闻评分，并返回 JSON 格式：
{{
  "filtered_news": [
    {{
      "id": 0,
      "score": 8,
      "reason": "关于个人养老金政策调整的权威报道"
    }}
  ]
}}

只返回评分 >= {self.relevance_threshold} 的新闻。
"""
            
            print(f"[AI] 正在调用 Gemini {self.gemini_model_name} 进行智能筛选...")
            
            # 调用 Gemini（添加重试机制）
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = model.generate_content(prompt)
                    
                    # 解析响应
                    response_text = response.text.strip()
                    
                    # 提取 JSON（去除可能的 markdown 代码块标记）
                    if "```json" in response_text:
                        response_text = response_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in response_text:
                        response_text = response_text.split("```")[1].split("```")[0].strip()
                    
                    result = json.loads(response_text)
                    filtered_ids = [item["id"] for item in result.get("filtered_news", [])]
                    
                    # 返回筛选后的新闻
                    filtered_news = [news_list[idx] for idx in filtered_ids if idx < len(news_list)]
                    
                    # 输出筛选详情
                    print(f"   [成功] Gemini 分析完成，保留 {len(filtered_news)}/{len(news_list)} 条")
                    for item in result.get("filtered_news", [])[:3]:  # 显示前3条
                        print(f"      • ID {item['id']} (评分: {item['score']}/10): {item['reason']}")
                    if len(result.get("filtered_news", [])) > 3:
                        print(f"      ... 还有 {len(result.get('filtered_news', [])) - 3} 条")
                    
                    return filtered_news
                
                except json.JSONDecodeError as e:
                    if attempt < max_retries - 1:
                        print(f"   [警告] JSON 解析失败，重试 ({attempt + 1}/{max_retries})...")
                        print(f"   响应内容: {response_text[:200]}...")
                        time.sleep(1)
                        continue
                    else:
                        print(f"   [错误] JSON 解析失败: {e}")
                        # 降级策略：返回所有结果
                        print("   [警告] 降级策略：返回所有搜索结果")
                        return news_list
                
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"   [警告] Gemini 调用失败，重试 ({attempt + 1}/{max_retries})...")
                        time.sleep(2)
                        continue
                    else:
                        print(f"   [错误] Gemini 调用失败: {e}")
                        # 降级策略：返回所有结果
                        return news_list
            
            return news_list
            
        except Exception as e:
            print(f"[错误] Gemini 筛选失败: {e}")
            # 降级策略：返回所有结果
            return news_list
    
    def _format_results(self, news_list: List[Dict]) -> List[Dict]:
        """
        将搜索结果转换为与热搜数据一致的格式
        
        Args:
            news_list: 原始新闻列表
            
        Returns:
            格式化后的新闻列表
        """
        formatted = []
        
        for news in news_list:
            try:
                # 转换为统一格式
                formatted_item = {
                    "title": news.get("title", ""),
                    "url": news.get("link", ""),
                    "mobileUrl": news.get("link", ""),  # Serper 没有单独的移动端链接
                    "source": "AI智能搜索",
                    "platform_id": "ai_search",
                    "rank": 0,  # AI 搜索的结果没有排名
                    "ranks": [],
                    "source_type": "ai_search",
                    "original_source": news.get("source", "未知来源"),
                    "date": news.get("date", ""),
                    "snippet": news.get("snippet", "")
                }
                formatted.append(formatted_item)
            except Exception as e:
                print(f"   [警告] 格式化新闻失败: {e}")
                continue
        
        return formatted


def search_pension_news_with_ai(config: Dict) -> List[Dict]:
    """
    便捷函数：搜索养老资讯
    
    Args:
        config: 配置字典
        
    Returns:
        养老资讯列表
    """
    try:
        ai_config = config.get("AI_SEARCH", {})
        
        # 检查是否启用
        if not ai_config.get("ENABLED", False):
            return []
        
        # 检查 API Keys
        if not ai_config.get("SERPER_API_KEY") or not ai_config.get("GEMINI_API_KEY"):
            print("[警告] AI 搜索功能已启用但未配置 API Keys，跳过")
            return []
        
        # 执行搜索
        manager = AISearchManager(config)
        results = manager.search_and_filter()
        
        return results
        
    except Exception as e:
        print(f"[错误] AI 搜索出错: {e}")
        return []

