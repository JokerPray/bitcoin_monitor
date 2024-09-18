import asyncio
import aiofiles
import csv
import aiohttp
from decimal import Decimal
from tortoise import Tortoise, run_async
from models import PriceRecord
from utils import fetch_price, send_email
from config import DATABASE_URL
import schedule
import time
from datetime import datetime, timezone

PAIRS = ["BTCUSDT", "BTCETH", "BTCXMR", "BTCSOL", "BTCRUB", "BTCDOGE"]
PREVIOUS_PRICES = {}

async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

async def monitor_prices():
    global PREVIOUS_PRICES
    async with aiohttp.ClientSession() as session:
        for pair in PAIRS:
            price = await fetch_price(session, pair)
            prev_price = PREVIOUS_PRICES.get(pair)
            if prev_price:
                difference = ((price - prev_price) / prev_price) * 100
                if difference >= 0.03:
                    # Отправляем email
                    subject = f"Цена {pair} выросла на {difference:.4f}%"
                    content = (
                        f"Текущая цена: {price}\n"
                        f"Предыдущая цена: {prev_price}\n"
                        f"Разница: {difference:.4f}%\n"
                        f"Время: {datetime.now(timezone.utc).isoformat()}"
                    )
                    await send_email(subject, content)
                    # Записываем в CSV
                    await log_to_csv(pair, price, difference)
                    # Сохраняем в базу
                    await save_to_db(pair, price, difference)
            else:
                difference = 0
                # Первые данные, можно также сохранять
                await save_to_db(pair, price, difference)
            PREVIOUS_PRICES[pair] = price

async def log_to_csv(title, price, difference):
    file_exists = False
    try:
        async with aiofiles.open('price_changes.csv', mode='r'):
            file_exists = True
    except FileNotFoundError:
        pass

    async with aiofiles.open('price_changes.csv', mode='a', newline='') as file:
        if not file_exists:
            header = ["title", "price", "max price", "min price", "date ISOformat", "difference", "total amount"]
            header_line = ','.join(header) + '\n'
            await file.write(header_line)
        date_iso = datetime.now(timezone.utc).isoformat()
        data_row = [title, str(price), "", "", date_iso, str(difference), ""]
        data_line = ','.join(data_row) + '\n'
        await file.write(data_line)

async def save_to_db(title, price, difference):
    # Получаем предыдущий рекорд для вычисления max и min
    previous_record = await PriceRecord.filter(title=title).order_by('-date').first()
    if previous_record:
        max_price = max(price, previous_record.max_price)
        min_price = min(price, previous_record.min_price)
    else:
        max_price = price
        min_price = price

    record = await PriceRecord.create(
        title=title,
        price=price,
        max_price=max_price,
        min_price=min_price,
        difference=difference,
        total_amount=price,  # Здесь можно добавить логику расчёта общей суммы
        coins={"BTC": title.replace("BTC", "")},
        date=datetime.now(timezone.utc)
    )

def job():
    asyncio.run(monitor_prices())

def main():
    run_async(init())
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()