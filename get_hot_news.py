import requests
import json
import time
import random
from datetime import datetime
import os

# 热点新闻平台列表
PLATFORMS = [
    '哔哩哔哩', '百度', '知乎', '百度贴吧', '少数派', 'IT之家',
    '澎湃新闻', '今日头条', '微博热搜', '36氪', '稀土掘金', '腾讯新闻'
]

# API基础URL
BASE_URL = 'https://api.pearktrue.cn/api/dailyhot'

def get_hot_news(platform):
    """获取指定平台的热点新闻"""
    try:
        url = f'{BASE_URL}/?title={platform}'
        response = requests.get(url)
        data = response.json()
        
        if data.get('code') == 200 and 'data' in data:
            # 提取title和desc
            cleaned_data = [
                {"title": item.get("title", ""),
                 "desc": item.get("desc", "")}
                for item in data['data']
                if isinstance(item, dict)
            ]
            return cleaned_data
        return []
    except Exception as e:
        print(f"获取{platform}热点新闻时出错: {str(e)}")
        return []

def save_to_json(data):
    """保存数据到JSON文件"""
    # 使用当前时间创建文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'hot_news_{timestamp}.json'
    
    # 保存到仓库根目录
    filepath = filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filepath}")
    except Exception as e:
        print(f"保存数据时出错: {str(e)}")

def main():
    all_platform_data = {}
    
    for platform in PLATFORMS:
        print(f"正在获取{platform}的热点新闻...")
        
        # 获取该平台的热点新闻
        platform_data = get_hot_news(platform)
        if platform_data:
            all_platform_data[platform] = platform_data
        
        # 随机休眠1-3秒
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
    
    # 如果获取到数据，保存到文件
    if all_platform_data:
        save_to_json(all_platform_data)
    else:
        print("未获取到任何数据")

if __name__ == '__main__':
    main()