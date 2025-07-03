# Sm Neverland - V2Ray Telegram Scraper

این پروژه به صورت خودکار کانفیگ‌های V2Ray/VMess/VLESS را از کانال‌های عمومی تلگرام استخراج می‌کند و در یک فایل Subscribe به نام `v2ray_configs.txt` ذخیره می‌کند.

## اجرای پروژه

```bash
pip install requests beautifulsoup4
python config_scraper.py
```

## استفاده در کلاینت‌ها

پس از اجرای اسکریپت، فایل `v2ray_configs.txt` را در GitHub آپلود کرده و لینک raw آن را در بخش Subscription برنامه‌هایی مثل V2RayNG وارد کنید.
