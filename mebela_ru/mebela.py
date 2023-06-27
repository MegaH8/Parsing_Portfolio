#import requests
#from lxml import html
#from bs4 import BeautifulSoup
#import pandas as pd


def main():
    with open('products_url.txt', encoding='utf-8-sig') as file:
        lines = [line.split()[0] for line in file.readlines()]

        count = 0
        urls = []
        names = []
        collors = []
        imgs = []

        for line in lines:
            q = requests.get(str(line))
            result = q.content

            soup = BeautifulSoup(result, 'lxml')
            product_url = line
            product_name = soup.find(class_='low').text
            for color_img in soup.find(class_='jcarousel-x').find_all('img'):
                product_text = color_img['alt']
                product_img = color_img['src']

                urls.append(product_url)
                names.append(product_name)
                collors.append(product_text)
                imgs.append(product_img)
                count += 1
                print(f'товаров добавлено {count}')

            data = {
                'url': urls,
                'имя': names,
                'цвет': collors,
                'ссылка': imgs
            }

    z = pd.DataFrame(data)
    z.to_excel("mebela_data.xlsx", index=False)


#if __name__ == '__main__':
#    main()
