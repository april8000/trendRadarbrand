}
payload = {
    'q': '养老保险政策',
    'num': 5,
    'gl': 'cn',
    'hl': 'zh-cn'
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        news = data.get('news', [])
        print(f'✓ Serper API 测试成功，返回 {len(news)} 条结果')
        if news:
            print(f'\n第一条新闻：')
            print(f'  标题：{news[0].get(\"title\", \"\")}')
            print(f'  来源：{news[0].get(\"source\", \"\")}')
            print(f'  时间：{news[0].get(\"date\", \"\")}')
    else:
        print(f'✗ 错误：{response.text}')
except Exception as e:
    print(f'✗ 错误：{e}')
"@ | Out-File -Encoding UTF8 test_serper.py

# 运行测试
python test_serper.py