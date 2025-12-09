# coding=utf-8

"""
AI 搜索功能测试脚本
用于测试 Serper API 和 Gemini AI 的搜索和筛选功能
"""

import os
import sys

def test_ai_search():
    """测试 AI 搜索功能"""
    
    print("="*60)
    print("AI 智能搜索功能测试")
    print("="*60 + "\n")
    
    # 检查环境变量
    serper_key = os.environ.get("SERPER_API_KEY", "")
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    
    if not serper_key:
        print("❌ 错误：未设置 SERPER_API_KEY 环境变量")
        print("\n请先设置环境变量：")
        print("  Windows: set SERPER_API_KEY=你的密钥")
        print("  Linux/Mac: export SERPER_API_KEY=你的密钥")
        return False
    
    if not gemini_key:
        print("❌ 错误：未设置 GEMINI_API_KEY 环境变量")
        print("\n请先设置环境变量：")
        print("  Windows: set GEMINI_API_KEY=你的密钥")
        print("  Linux/Mac: export GEMINI_API_KEY=你的密钥")
        return False
    
    print("✅ 环境变量配置检查通过")
    print(f"   SERPER_API_KEY: {serper_key[:10]}...{serper_key[-5:]}")
    print(f"   GEMINI_API_KEY: {gemini_key[:10]}...{gemini_key[-5:]}")
    print()
    
    # 导入模块
    try:
        from main import load_config
        from ai_search import search_pension_news_with_ai
        print("✅ 模块导入成功")
        print()
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("\n请确保已安装所有依赖：")
        print("  pip install -r requirements.txt")
        return False
    
    # 加载配置
    try:
        config = load_config()
        print("✅ 配置加载成功")
        print()
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    # 检查 AI 搜索是否启用
    if not config.get("AI_SEARCH", {}).get("ENABLED", False):
        print("⚠️ 警告：AI 搜索功能未启用")
        print("\n请在 config/config.yaml 中设置：")
        print("  ai_search:")
        print("    enabled: true")
        print()
        choice = input("是否继续测试？(y/n): ")
        if choice.lower() != 'y':
            return False
        print()
    
    # 执行 AI 搜索
    print("开始执行 AI 搜索测试...")
    print()
    
    try:
        results = search_pension_news_with_ai(config)
        
        if not results:
            print("\n⚠️ 搜索未返回结果")
            print("\n可能的原因：")
            print("  1. Serper API 调用失败（检查 API Key 是否正确）")
            print("  2. Gemini 筛选过于严格（所有新闻都被过滤）")
            print("  3. 过去24小时内确实没有相关新闻")
            return False
        
        print(f"\n{'='*60}")
        print(f"✅ 测试成功！共获取 {len(results)} 条养老资讯")
        print(f"{'='*60}\n")
        
        # 显示结果
        print("搜索结果预览（前5条）：\n")
        for idx, item in enumerate(results[:5], 1):
            print(f"{idx}. {item['title']}")
            print(f"   来源：{item.get('original_source', '未知')}")
            print(f"   时间：{item.get('date', '未知')}")
            print(f"   链接：{item['url'][:80]}...")
            if item.get('snippet'):
                snippet = item['snippet'][:100]
                print(f"   摘要：{snippet}...")
            print()
        
        if len(results) > 5:
            print(f"... 还有 {len(results) - 5} 条结果\n")
        
        # 统计信息
        print(f"{'='*60}")
        print("统计信息：")
        print(f"  • 总结果数：{len(results)}")
        print(f"  • 数据来源：AI智能搜索")
        print(f"  • 搜索关键词：{', '.join(config['AI_SEARCH']['SEARCH_KEYWORDS'][:3])}等")
        print(f"  • 时间范围：过去 {config['AI_SEARCH']['TIME_RANGE_HOURS']} 小时")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查：")
        print("  1. API Keys 是否正确")
        print("  2. 网络连接是否正常")
        print("  3. API 配额是否用完")
        import traceback
        print("\n详细错误信息：")
        traceback.print_exc()
        return False


def main():
    """主函数"""
    success = test_ai_search()
    
    if success:
        print("🎉 所有测试通过！")
        print("\nAI 搜索功能已就绪，可以开始使用。")
        print("\n下一步：")
        print("  1. 运行主程序：python main.py")
        print("  2. 查看详细文档：AI_SEARCH_README.md")
    else:
        print("\n❌ 测试未通过，请根据上述提示解决问题。")
        print("\n如需帮助，请查看 AI_SEARCH_README.md 中的常见问题部分。")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())



