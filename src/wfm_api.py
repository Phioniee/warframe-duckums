import requests
import json

API_BASE_URL = "https://api.warframe.market/v2"

# Standard headers for V2 API requests
HEADERS = {
    "accept": "application/json",
    "Platform": "pc",
    "Language": "en"
}

def get_prime_parts_list():
    """Fetch the list of all prime parts from the API."""
    endpoint = f"{API_BASE_URL}/items"

    try:
        response = requests.get(endpoint, headers=HEADERS, timeout=15)
        response.raise_for_status()
        full_items_list = response.json()

        prime_parts = []
        for item in full_items_list:
            item_name = item.get('i18n', {}).get('en', {}).get('name', '')
            if 'Prime' in item_name:
                prime_parts.append(item)
        return prime_parts

    except requests.exceptions.RequestException as e:
        return None
    
    except json.JSONDecodeError:
        return None

def get_price(slug: str):
    """Calculate the average price of slug's top 5 online cheapest sell orders."""
    endpoint = f"{API_BASE_URL}/item/{slug}/orders"

    try:
        response = requests.get(endpoint, headers=HEADERS, timeout=10)
        response.raise_for_status()
        all_orders = response.json().get('data', {}).get('orders', [])

        online_sell_orders = [
            order for order in all_orders
            if order.get('order_type') == 'sell' and order.get('user', {}).get('status') == 'ingame' and order.get('visible', False)
        ]
        if not online_sell_orders:
            return None
        
        sorted_orders = sorted(online_sell_orders, key=lambda x: x.get('platinum', float('inf')))
        top_5_orders = sorted_orders[:5]
        
        average_price = sum([order['platinum'] for order in top_5_orders]) / len(top_5_orders)
        return int(average_price)
    
    except requests.exceptions.RequestException as e:
        return None
    
    except json.JSONDecodeError:
        return None