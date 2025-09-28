import requests
import json
import time
import random
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 邮箱配置参数
EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',  # QQ邮箱SMTP服务器，可根据需要修改
    'smtp_port': 587,
    'sender_email': '32580117@qq.com',  # 发送方邮箱
    'sender_password': 'khashmdhmgqobjhb',  # 邮箱授权码
    'receiver_email': 'jor-z@foxmail.com'  # 接收方邮箱
}

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

def send_email(data):
    """发送热点新闻数据到指定邮箱"""
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = Header(f"热点新闻助手 <{EMAIL_CONFIG['sender_email']}>", 'utf-8')
        msg['To'] = Header(EMAIL_CONFIG['receiver_email'], 'utf-8')
        
        # 生成邮件主题
        timestamp = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        msg['Subject'] = Header(f"每日热点新闻汇总 - {timestamp}", 'utf-8')
        
        # 生成邮件内容
        html_content = generate_html_content(data, timestamp)
        
        # 添加HTML内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 连接SMTP服务器并发送邮件
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()  # 启用TLS加密
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['receiver_email'], text)
        server.quit()
        
        print(f"热点新闻已成功发送到: {EMAIL_CONFIG['receiver_email']}")
        
    except Exception as e:
        print(f"发送邮件时出错: {str(e)}")

def generate_html_content(data, timestamp):
    """生成HTML格式的邮件内容"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; margin-bottom: 20px; }}
            .platform {{ margin-bottom: 30px; }}
            .platform-title {{ background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; font-size: 18px; font-weight: bold; }}
            .news-item {{ background-color: #f9f9f9; margin: 10px 0; padding: 15px; border-left: 4px solid #4CAF50; border-radius: 0 5px 5px 0; }}
            .news-title {{ font-weight: bold; color: #333; margin-bottom: 5px; }}
            .news-desc {{ color: #666; font-size: 14px; line-height: 1.4; }}
            .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📰 每日热点新闻汇总</h1>
                <p>更新时间: {timestamp}</p>
            </div>
    """
    
    for platform, news_list in data.items():
        html += f'<div class="platform"><div class="platform-title">🔥 {platform}</div>'
        
        for news in news_list[:10]:  # 限制每个平台显示前10条
            title = news.get('title', '').strip()
            desc = news.get('desc', '').strip()
            
            if title:
                html += f"""
                <div class="news-item">
                    <div class="news-title">{title}</div>
                    {f'<div class="news-desc">{desc}</div>' if desc else ''}
                </div>
                """
        
        html += '</div>'
    
    html += """
            <div class="footer">
                <p>📧 本邮件由热点新闻助手自动发送</p>
                <p>数据来源: PearAPI</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

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
    
    # 如果获取到数据，发送邮件
    if all_platform_data:
        send_email(all_platform_data)
    else:
        print("未获取到任何数据")

if __name__ == '__main__':
    main()