import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://prices.db")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.yandex.ru")  # Пример для Gmail SMTP
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USER = os.getenv("EMAIL_USER", "your_email@yandex.ru")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "password")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "Some_email@yandex.ru")