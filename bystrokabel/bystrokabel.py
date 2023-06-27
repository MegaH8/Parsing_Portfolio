import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html

j = 1
search_query = input()
names = []
design_weights = []
out_diameter = []
min_reel = []
max_len_per_coil = []
for i in range(20):
    req = requests.get(f'https://bystrokabel.ru/character/search?query={search_query}&page={i+1}')
    src = req.text

# тестовый HTML
#with open('bystrokabel.html', 'w', encoding='utf-8-sig') as file:
#    file.write(src)
#with open('bystrokabel.html', 'r', encoding='utf-8-sig') as file:
#    src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    kabels_data = soup.find(class_='result-table').find_all("tr")
    for line in kabels_data:
        product_tds = line.find_all('td', class_=True)
        if product_tds != []:
            names.append(product_tds[0].text)
            design_weights.append(product_tds[3].text)
            out_diameter.append(product_tds[4].text)
            chetyr = '№' + product_tds[5].text.split('№')[1]
            min_reel.append(chetyr)
            max_len_per_coil.append(product_tds[6].text)
            print(f'Количество итераций {j}')
            j += 1
kabel_data = {
        'Наименование': names,
        'Расчетная масса, кг/км': design_weights,
        'Наружный диаметр, мм': out_diameter,
        'Минимальный барабан': min_reel,
        'Макс. длина в бухте': max_len_per_coil
        }


data_frame = pd.DataFrame(kabel_data)
data_frame.to_excel(f"bystrokabel_{search_query}.xlsx", index=False)
