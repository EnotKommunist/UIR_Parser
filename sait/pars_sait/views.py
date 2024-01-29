from django.shortcuts import render, redirect
from pars_sait.models import ParsInfo

##############
import csv

import requests
import pandas as pd
import sqlite3
import io
###############


def print_db(request):
    info = ParsInfo.objects.all()
    return render(request, 'print_db.html', {'info': info})


def index_page(request):
    return render(request, 'index.html')


def get_category(zap):
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
        'query': f'{zap}',
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
                'salePriceU': float(prod.get('salePriceU', None)) / 100 if prod.get('salePriceU',
                                                                                    None) != None else None,
                'priceU': float(prod.get('priceU', None)) / 100 if prod.get('priceU', None) != None else None,
                'sale': prod.get('sale', None),
                'rating': prod.get('reviewRating', None),
                'feedbacks': prod.get('feedbacks', None),
                'supplier': prod.get('supplier', None),
                'supplierRating': prod.get('supplierRating', None),
                'link': f'https://www.wildberries.ru/catalog/{prod.get("id", None)}/detail.aspx',
            })
    return products


def main(zap):
    zap = zap
    response = get_category(zap)
    products = prepare_items(response)
    pd.DataFrame(products).to_csv('products.csv', index=False)
    path = "products.csv"
    reader = list(csv.reader(open(path, encoding='utf-8'), delimiter=','))
    writer = csv.writer(open(path, 'w', encoding='utf-8'), delimiter=';')
    writer.writerows(row for row in reader)
    lines = []
    with io.open('products.csv', encoding='utf-8') as file:
        for line in file:
            lines.append(line.split(';'))
    lines = lines[1:]
    l = []
    for i in range(len(lines)):
        if i % 2 != 0:
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
    return lines


def input_page(request):
    return render(request, 'btn.html')

def parse_page(request):
    if request.method == 'POST':
        input_string = request.POST.get('input_string')
        a = main(input_string)
        for i in range(1, len(a) + 1):
            new_pars_info = ParsInfo(id=i, brand=a[i - 1][0], name=a[i - 1][1], id_seller=a[i - 1][2],
                                     discounted_price=a[i - 1][3], original_price=a[i - 1][4],
                                     discount_percentage=a[i - 1][5], product_rating=a[i - 1][6],
                                     number_of_reviews=a[i - 1][7], supplier=a[i - 1][8], supplier_rating=a[i - 1][9],
                                     link=a[i - 1][10])
            new_pars_info.save()
        return render(request, 'result_page.html')