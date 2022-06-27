import requests
from bs4 import BeautifulSoup
import sourcer
import time
import os


url = 'https://www.bbc.co.uk/news/'
base_url = 'https://www.bbc.co.uk'
links = []


def read_links(links):
    for link in links:
        sourcer.set_url(link)
        os.system
        input("Press Key to Continue")
        os.system('cls||clear')

def open_link(url, timeout_start=''):
    req = requests.get(url).content
    soup = BeautifulSoup(req, 'html.parser')
    # print(soup.head)
    index_errors = []
    timeout = 3
    if not timeout_start:
        timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        for data in soup.find_all('h3'):
            link = data.find_parents("a")
            try:
                if link[0]['href']:
                    uri = link[0]['href']
                    slug = uri.split('/')[1]
                    reference = uri.split('/')[-1]
                    print(uri)
                    print(slug)
                    print(reference)
                    clicked_links = []
                    if slug == 'news' or slug == 'sport':
                        if reference not in clicked_links:
                            links.append(base_url+uri)
                            clicked_links.append(reference)
                print(data.get_text())
                print('\n')
            except IndexError:
                    index_errors.append(data)
        if time.time() < timeout_start +timeout:
            for l in links:
                open_link(l, timeout_start)
            print(index_errors)
    input("Press Key to Continue")
    os.system('cls||clear')
    read_links(list(dict.fromkeys(links)))

open_link(url)




# for data in soup.find_all('a'):
#     print(data.get_text())
#     print('\n')