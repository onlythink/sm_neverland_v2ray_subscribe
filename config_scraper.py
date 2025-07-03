import requests
from bs4 import BeautifulSoup
import re

MAX_LINKS_PER_CHANNEL = 20
CHANNEL_FILE = "channels.txt"
OUTPUT_FILE = "v2ray_configs.txt"

# پترن‌های لینک کانفیگ
patterns = [
    r'vmess://[a-zA-Z0-9+/=._-]+',
    r'vless://[a-zA-Z0-9@:/?=&#._-]+',
    r'trojan://[a-zA-Z0-9@:/?=&#._-]+',
    r'shadowsocks://[a-zA-Z0-9@:/?=&#._-]+',
]

def extract_links_from_channel(url):
    print(f"🔍 استخراج از: {url}")
    try:
        res = requests.get(url, timeout=15)
        if res.status_code != 200:
            print(f"❌ خطا در خواندن {url} (کد {res.status_code})")
            return []
        soup = BeautifulSoup(res.text, "html.parser")
        code_tags = soup.find_all("code")
        links = []
        for code_tag in code_tags:
            text = code_tag.get_text()
            for pattern in patterns:
                found = re.findall(pattern, text)
                for link in found:
                    if link not in links:
                        links.append(link)
                    if len(links) >= MAX_LINKS_PER_CHANNEL:
                        break
            if len(links) >= MAX_LINKS_PER_CHANNEL:
                break
        return links[:MAX_LINKS_PER_CHANNEL]
    except Exception as e:
        print(f"❌ خطا در پردازش {url}: {e}")
        return []

def main():
    all_links = []
    with open(CHANNEL_FILE, "r", encoding="utf-8") as f:
        channels = [line.strip() for line in f if line.strip()]
    for ch in channels:
        # مطمئن شو لینک قالب https://t.me/s/channelname هست
        if not ch.startswith("https://t.me/s/"):
            if ch.startswith("https://t.me/"):
                ch = ch.replace("https://t.me/", "https://t.me/s/")
            else:
                print(f"⚠️ فرمت لینک نامعتبر است: {ch}")
                continue
        links = extract_links_from_channel(ch)
        all_links.extend(links)
    # حذف تکراری‌ها
    all_links = list(dict.fromkeys(all_links))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(link.strip() + "\n")
    print(f"\n✅ جمع‌آوری کامل شد. {len(all_links)} کانفیگ ذخیره شد در: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
