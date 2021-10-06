import requests
from bs4 import BeautifulSoup


def get_eng_name(ru_name):
    '''The function receives as input the name of a foreign actor or director in Russian and returns his name in English taken from the wiki'''
    URL = 'https://ru.wikipedia.org/wiki/'
    first_name, last_name = ru_name.split()
    response = requests.get(f'{URL}{last_name},_{first_name}')
    soup = BeautifulSoup(response.text, 'html.parser')
    eng_name = soup.find('span', lang="en").text
    return eng_name.lower().replace(' ', '_')