import requests
from bs4 import BeautifulSoup
import re

MAX_LINKS_PER_CHANNEL = 20
CHANNEL_FILE = "channels.txt"
OUTPUT_FILE = "v2ray_configs.txt"

patterns = [
    r'vmess://[a-zA-Z0-9+/=._-]+',
    r'vless://[a-zA-Z0-9@:/?=&#._-]+',
    r'trojan://[a-zA-Z0-9@:/?=&#._-]+',
    r'shadowsocks://[a-zA-Z0-9@:/?=&#._-]+',
]

def extract_links_from_channel(url):
    print(f"🔍 استخراج از: {url}")
    res = requests.get(url)
    if res.status_code != 200:
        print(f"❌ خطا در خواندن {url}")
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    messages = soup.find_all("div", class_="tgme_widget_message_text")
    links = []
    for msg in messages:
        text = msg.get_text()
        for pattern in patterns:
            found = re.findall(pattern, text)
            for link in found:
                if link not in links:
                    links.append(link)
        if len(links) >= MAX_LINKS_PER_CHANNEL:
            break
    return links[:MAX_LINKS_PER_CHANNEL]

def main():
    all_links = []
    with open(CHANNEL_FILE, "r") as f:
        channels = f.read().splitlines()
    for ch in channels:
        links = extract_links_from_channel(ch)
        all_links.extend(links)
    all_links = list(dict.fromkeys(all_links))
    
    # تبدیل لیست به رشته با جداکننده خط جدید
    all_configs = "\n".join(all_links)
    
    # نوشتن کل رشته در فایل خروجی
    output_file = OUTPUT_FILE
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_configs)
    
    print(f"\n✅ جمع‌آوری کامل شد. {len(all_links)} کانفیگ ذخیره شد در: {output_file}")

if __name__ == "__main__":
    main()
