import pandas as pd
import requests


def get_category():
    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&query=iphone%2013&resultset=catalog&sort=popular&spp=29&suppressSpellcheck=false'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "YaBrowser";v="23.11", "Not=A?Brand";v="99", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
    }
    response = requests.get(url=url, headers=headers)
    return response.json()

def prepare_items(response):
    products = []
    prod_raw = response.get('data', {}).get('products', None)
    if prod_raw != None and len(prod_raw) > 0:
        for prod in prod_raw:
            products.append({
                'brand': prod.get('brand', None),
                'name': prod.get('name', None),
                'sale': prod.get('sale', None),
                'id': prod.get('id', None),
                'priceU': float(prod.get('priceU', None)) / 100 if prod.get('priceU', None) != None else None,
                'salePriceU': float(prod.get('salePriceU', None)) / 100 if prod.get('salePriceU', None) != None else None
            })
    return products


def main():
    response = get_category()
    products = prepare_items(response)
    print(products)
    pd.DataFrame(products).to_csv('products.csv', index=False)


if __name__ == '__main__':
    main()
