from celery import shared_task
import requests
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime


down_sites = set()
URLS_TO_PING = [
    "https://apnamarket143.vercel.app/",
    "https://king143nd.pythonanywhere.com/",
    "https://adda-travelling.vercel.app/",
    "https://magic-text-enhancer.vercel.app/",
]

@shared_task
def ping_all_sites():
    for url in URLS_TO_PING:
        if url in down_sites:
            print(f"⏭ Skipping {url} (previously marked down)")
            continue
        try:
            response = requests.get(url, timeout=10)
            print(f"Pinged {url}: {response.status_code}")
        except Exception as e:
            print(f"Failed to ping {url}: {e}")
            send_mail(
                subject="🚨 Website Down Alert",
                message=f"The following site is down:\n\n{url}\n\nError: {str(e)}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            down_sites.add(url)


@shared_task
def daily_site_report():
    report_lines = [f"📝 Daily Website Status Report – {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

    for url in URLS_TO_PING:
        try:
            response = requests.get(url, timeout=10)
            status = response.status_code
            elapsed = response.elapsed.total_seconds()
            report_lines.append(f"✅ {url} - Status: {status}, Time: {elapsed:.2f}s")
        except Exception as e:
            report_lines.append(f"❌ {url} - Failed: {str(e)}")

    email_body = "\n".join(report_lines)

    send_mail(
        subject="🌐 Daily Report – Website Ping Status",
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )