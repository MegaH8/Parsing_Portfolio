from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import html
from bs4 import BeautifulSoup
from time import sleep

# беру полный html с ссылками всех товаров
driver = webdriver.Firefox()
driver.get('https://www.mebela.ru/catalog/mebel-dlya-personala/')


#all html

xpath_quest = '//*[@id="allCatalogBlock"]/div[3]/div[1]/div/ul/li[last()-1]/a'
count_pages = int(driver.find_element(By.XPATH, xpath_quest).text)
print(count_pages)
for page in range(count_pages - 1):
        driver.find_element(By.XPATH, '//*[@id="ajax_nav_1"]/span').click()
        sleep(10)
src = driver.page_source
with open('mebela.html', 'w', encoding='utf-8-sig') as f:
    f.write(src)


# достаю ссылки
products_url = []

with open('mebela.html', encoding='utf-8-sig') as f:
    src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    products = soup.find_all('a', class_='cat-link2 cat-link2-new')
    for product in products:
        product_url = product.get('href')
        print(product_url)
        products_url.append(product_url)
    with open('products_url.txt', 'a', encoding='utf-8-sig') as file:
        for line in products_url:
            file.write(f'https://www.mebela.ru{line}\n')
