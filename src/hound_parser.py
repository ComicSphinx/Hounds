# @Author: Daniil Maslov (ComicSphinx)

import requests
from bs4 import BeautifulSoup as bs

def get_page():
    link = 'link'
    
    return (requests.get(link))

def parse_cost():
    page = get_page()
    data = bs(page.text, 'html.parser')
    cost = data.find('span', class_= 'dashboard-currency dashboard-card-big-nums rub')

    return cost.text

def parse_income():
    page = get_page()
    data = bs(page.text, 'html.parser')

    income = data.find('div', class_= 'flex dashboard-item xl3 lg3 md6 sm6 xs12 align-content-start')
    income = income.find('span', class_= 'dashboard-currency dashboard-card-big-nums rub')

    return income.text
