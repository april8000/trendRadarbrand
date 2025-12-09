# coding=utf-8
"""
测试 Gemini 模型可用性
"""

import os
import sys
import time
import warnings

# 忽略 Python 版本警告
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
except Exception as e:
    print(f"[错误] 导入 google.generativeai 失败: {e}")
    print("   请运行: pip install google-generativeai")
    sys.exit(1)

# 设置控制台编码为 UTF-8（Windows）
if sys.platform == "win32":
    try:
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
    except:
        pass

# 从环境变量获取 API Key（测试时也可以硬编码）
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# 如果环境变量未设置，尝试使用硬编码的值（仅用于测试）
if not GEMINI_API_KEY:
    GEMINI_API_KEY = "AIzaSyAIioOXA5w0Zoez_fBsNuFBxAVzjgHpJMs"
    print("[提示] 使用硬编码的 API Key（仅用于测试）")
if not GEMINI_API_KEY:
    print("[错误] 请设置环境变量 GEMINI_API_KEY")
    print("   Windows PowerShell: $env:GEMINI_API_KEY = '你的API_Key'")
    print("   Linux/Mac: export GEMINI_API_KEY='你的API_Key'")
    sys.exit(1)

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"[错误] 配置 Gemini API 失败: {e}")
    sys.exit(1)

# 要测试的模型列表
MODELS_TO_TEST = [
    "gemini-pro",
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-latest",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp",
]

print("=" * 60)
print("测试 Gemini 模型可用性")
print("=" * 60)
print()

# 跳过 list_models()（容易超时），直接测试预设列表
print("[信息] 直接测试预设模型列表（跳过列表查询以避免超时）")
print()

test_prompt = "你好"

successful_models = []

# 只测试最常用的几个模型，减少超时风险
PRIORITY_MODELS = [
    "gemini-pro",
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
]

# 先测试优先级模型
models_to_test = PRIORITY_MODELS + [m for m in MODELS_TO_TEST if m not in PRIORITY_MODELS]

for model_name in models_to_test:
    # 提取模型名称（去掉 models/ 前缀）
    clean_name = model_name.replace("models/", "")
    print(f"测试模型: {clean_name}...", end=" ", flush=True)
    
    # 添加重试机制
    max_retries = 2
    success = False
    
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(clean_name)
            # 尝试调用 API
            response = model.generate_content(test_prompt)
            result = response.text.strip()
            print(f"[成功]")
            print(f"   响应: {result[:50]}...")
            successful_models.append(clean_name)
            success = True
            break
        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries - 1:
                # 重试前等待
                time.sleep(1)
                continue
            else:
                # 最后一次尝试失败
                if "404" in error_msg or "not found" in error_msg.lower():
                    print(f"[失败] 模型不存在")
                elif "not supported" in error_msg.lower():
                    print(f"[失败] 模型不支持 generateContent")
                elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower() or "503" in error_msg:
                    print(f"[失败] 网络超时/连接失败")
                elif "403" in error_msg or "permission" in error_msg.lower():
                    print(f"[失败] API Key 权限不足")
                else:
                    print(f"[失败] {error_msg[:60]}...")
    
    print()

print("=" * 60)
print("测试完成")
print("=" * 60)
print()

if successful_models:
    print("[成功] 可用的模型列表:")
    for model in successful_models:
        print(f"   - {model}")
    print()
    print("[建议] 推荐使用的模型（按优先级）:")
    # 优先推荐更稳定的模型
    priority_models = ["gemini-pro", "gemini-1.5-flash", "gemini-1.5-pro"]
    for model in priority_models:
        if model in successful_models:
            print(f"   * {model} (推荐)")
            break
    else:
        print(f"   * {successful_models[0]} (第一个可用的)")
else:
    print("[错误] 没有找到可用的模型")
    print("   请检查:")
    print("   1. GEMINI_API_KEY 是否正确")
    print("   2. API Key 是否有访问 Gemini 的权限")
    print("   3. 网络连接是否正常")

