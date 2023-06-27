import requests
from bs4 import BeautifulSoup
from lxml import html
from time import sleep
import random
import json
import csv



#url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
#
headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
#req = requests.get(url)
#src = req.text
#
#with open('health.html', 'w', encoding='utf-8-sig') as f:
#    f.write(src)

#with open('health.html') as f:
#    src = f.read()
#
#soup = BeautifulSoup(src, 'lxml')
#all_products = soup.find_all(class_='mzr-tc-group-item-href')
#
#all_categories_dist = {}
#for i in all_products:
#    item_text = i.text
#    item_href = 'https://health-diet.ru' + i.get('href')
#
#    all_categories_dist[item_text] = item_href
#
#with open('all_categories_dist.json', 'w', encoding='utf-8-sig') as f:
#    json.dump(all_categories_dist, f, indent=4, ensure_ascii=False)

with open('all_categories_dist.json', encoding='utf-8-sig') as file:
    all_categories = json.load(file)


iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')

for category_name, category_href in all_categories.items():


    rep = [' ', ',', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')


    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8-sig') as file:
        file.write(src)

    with open(f'data/{count}_{category_name}.html', encoding='utf-8-sig') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    #Проверка страницы на наличие таблицы
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue


    #собираем заголовки таблицы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    protein = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', newline='' , encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                protein,
                fats,
                carbohydrates
            )
        )

    #собираем данные продукта
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = []
    for item in products_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        calories = product_tds[1].text
        protein = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        #Запись в Json
        product_info.append(
            {
                'Title': title,
                'Calories': calories,
                'Protein': protein,
                'Fats': fats,
                'Carbohydrates': carbohydrates
            }
        )

        with open(f'data/{count}_{category_name}.csv', 'a', newline='' , encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    protein,
                    fats,
                    carbohydrates
                )
            )
    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'№ Итерации {count}, {category_name} записан.')
    iteration_count -= 1
    if iteration_count == 0:
        print('Работа закончена')
        break
    print(f'Осталось итераций: {iteration_count}')
    sleep(random.randrange(2, 4))
