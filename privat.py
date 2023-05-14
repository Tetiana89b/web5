import argparse
import asyncio
from datetime import datetime, timedelta

import aiohttp


async def fetch_exchange_rates(days: int, currencies: list):
    async with aiohttp.ClientSession() as session:
        url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
        exchange_rates = []
        for i in range(days):
            date = (datetime.today() - timedelta(days=i)).strftime('%d.%m.%Y')
            async with session.get(url + date) as response:
                data = await response.json()
                rates = {
                    'date': date,
                    'rates': {}
                }
                for currency in currencies:
                    rate = next(
                        (item for item in data['exchangeRate'] if item['currency'] == currency), None)
                    if rate:
                        rates['rates'][currency] = {
                            'sale': rate['saleRateNB'],
                            'purchase': rate['purchaseRateNB']
                        }
                exchange_rates.append(rates)
        return exchange_rates

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Fetch exchange rates for selected currencies')
    parser.add_argument(
        'days', type=int, help='Number of days to fetch exchange rates for (up to 10)')
    parser.add_argument('--currencies', type=str, nargs='+', default=[
                        'USD', 'EUR'], help='Currencies to include in the response (default: USD, EUR)')
    args = parser.parse_args()

    if args.days > 10:
        print('Error: Maximum number of days to fetch exchange rates is 10')
    else:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            fetch_exchange_rates(args.days, args.currencies))
        print(result)
