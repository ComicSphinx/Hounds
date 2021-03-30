# @Author: Daniil Maslov (ComicSphinx)

import requests
from bs4 import BeautifulSoup as bs

def main():
    link = 'https://intelinvest.ru/public-portfolio/id' # instead of this link put your own public-portfolio link
    
    page = get_page(link)
    parse_data(page)

def get_page(link):
    return (requests.get(link))

def parse_data(page):
    data = bs(page.text, 'html.parser')
    
    cost = data.find('span', class_= 'dashboard-currency dashboard-card-big-nums rub')

    income = data.find('div', class_= 'flex dashboard-item xl3 lg3 md6 sm6 xs12 align-content-start')
    income = income.find('span', class_= 'dashboard-currency dashboard-card-big-nums rub')

    print(cost.text)
    print(income.text)
    

if __name__ == '__main__':
    main()