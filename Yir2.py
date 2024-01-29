import csv

import requests
import pandas as pd
import sqlite3
import io

a = str(input())
def get_category():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=i',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "YaBrowser";v="23.11", "Not=A?Brand";v="99", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'TestGroup': 'no_test',
        'TestID': 'no_test',
        'appType': '1',
        'curr': 'rub',
        'dest': '-1257786',
        'query': f'{a}',
        'resultset': 'catalog',
        'sort': 'popular',
        'spp': '29',
        'suppressSpellcheck': 'false',
    }

    response = requests.get('https://search.wb.ru/exactmatch/ru/common/v4/search', params=params, headers=headers)

    return response.json()

def prepare_items(response):
    products = []
    prod_raw = response.get('data', {}).get('products', None)
    if prod_raw != None and len(prod_raw) > 0:
        for prod in prod_raw:
            products.append({
                'brand': prod.get('brand', None),
                'name': prod.get('name', None),
                'id': prod.get('id', None),
                'salePriceU': float(prod.get('salePriceU', None)) / 100 if prod.get('salePriceU', None) != None else None,
                'priceU': float(prod.get('priceU', None)) / 100 if prod.get('priceU', None) != None else None,
                'sale': prod.get('sale', None),
                'rating': prod.get('reviewRating', None),
                'feedbacks': prod.get('feedbacks',None),
                'supplier': prod.get('supplier', None),
                'supplierRating': prod.get('supplierRating', None),
                'link': f'https://www.wildberries.ru/catalog/{prod.get("id", None)}/detail.aspx',
            })
    return products


def main():
    response = get_category()
    products = prepare_items(response)
    pd.DataFrame(products).to_csv('products.csv', index=False)
    path = "products.csv"
    reader = list(csv.reader(open(path, encoding='utf-8'), delimiter=','))
    writer = csv.writer(open(path, 'w', encoding='utf-8'), delimiter=';')
    writer.writerows(row for row in reader)
    connection = sqlite3.connect('YIR.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS yir (
    id INTEGER PRIMARY KEY autoincrement,
    
    brand TEXT NOT NULL,
    name TEXT NOT NULL,
    id_seller INTEGER NOT NULL,
    discounted_price REAL NOT NULL,
    original_price REAL NOT NULL,
    discount_percentage REAL NOT NULL,
    product_rating REAL NOT NULL,
    number_of_reviews INTEGER NOT NULL,
    supplier TEXT NOT NULL,
    supplier_rating REAL NOT NULL,
    link TEXT NOT NULL
    )
    ''')
    lines = []
    with io.open('products.csv', encoding='utf-8') as file:
        for line in file:
            lines.append(line.split(';'))
    lines = lines[1:]
    l = []
    for i in range(len(lines)):
        if i%2!=0:
            l.append(lines[i])
    lines = l
    for i in range(len(lines)):
        lines[i][2] = int(lines[i][2])
        lines[i][7] = int(lines[i][7])
        lines[i][3] = float(lines[i][3])
        lines[i][3] = float(lines[i][3])
        lines[i][4] = float(lines[i][4])
        lines[i][5] = float(lines[i][5])
        lines[i][6] = float(lines[i][6])
        lines[i][9] = float(lines[i][9])
    cursor.execute('DELETE FROM yir')
    for i in lines:
        cursor.execute('INSERT INTO yir (brand, name, id_seller, discounted_price, original_price, discount_percentage, product_rating, number_of_reviews, supplier, supplier_rating, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', i)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()



