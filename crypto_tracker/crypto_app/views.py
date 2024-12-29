from django.shortcuts import render
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def crypto_prices_view(request):
    # API URL and parameters
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '',  # Replace with your actual API key , I am usign coinmarketcap API cox its free
    }

    # Cryptocurrencies to track with entry prices
    desired_cryptos = {
        'CGPT': 0.2177,  # Example entry price for Coins
        'KAR': 0.5936,
        'ATLAS': 0.005889,
        'TET': 9.35,
        'MAVIA': 1.865,
        'GTAI': 1.068,
        'CSIX': 0.03,
        'SFUND': 2.26,
        'VOXEL': 0.268
    }

    session = Session()
    session.headers.update(headers)
    crypto_data = []

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        # Extract prices and calculate profit/loss
        for crypto in data.get('data', []):
            symbol = crypto['symbol']
            if symbol in desired_cryptos:
                current_price = crypto['quote']['USD']['price']
                entry_price = desired_cryptos[symbol]
                profit_loss = current_price - entry_price
                profit_loss_percentage = (profit_loss / entry_price) * 100

                # Append the data for display
                crypto_data.append({
                    'symbol': symbol,
                    'current_price': current_price,
                    'entry_price': entry_price,
                    'profit_loss': profit_loss,
                    'profit_loss_percentage': profit_loss_percentage
                })

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        crypto_data = [{'error': str(e)}]

    # Pass data to the template
    return render(request, 'crypto_prices.html', {'crypto_data': crypto_data})
