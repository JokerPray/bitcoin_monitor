import aiohttp
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL
from aiosmtplib import SMTP
from email.message import EmailMessage

async def fetch_price(session, pair):
    # Реализация запроса к API Binance
    api_url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    async with session.get(api_url) as response:
        data = await response.json()
        price = float(data.get("price", 0))
        return price

async def send_email(subject, content):
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = RECIPIENT_EMAIL
    message["Subject"] = subject
    message.set_content(content)
    smtp = SMTP(
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_USER,
        password=EMAIL_PASSWORD,
        use_tls=True,
    )

    await smtp.connect()
    await smtp.send_message(message)
    await smtp.quit()


    