from horse import HorseSpeedStats

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://knowyourhorses.com/horses/"

def create_soup(url: str) -> BeautifulSoup:
    page = requests.get(url)
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        return None
    
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def scrape_data(ctr: int) -> HorseSpeedStats:
    horse = HorseSpeedStats()
    speed_stats = create_soup(BASE_URL+str(ctr)+"/speed_statistics")
    j = 1000
    while j < 2800:
        horse.stats[j] = []
        j = j + 200
    
    table = speed_stats.find('table')
    temp = table.find_all('td')

    i = 0
    ref = 800  # Start on 800 because when i == 0, it will be +200
    while i < len(temp):
        if i % 9 == 0:
            ref = ref + 200
        horse.stats[ref].append(temp[i].text)
        i = i + 1

    # ancestry = create_soup(BASE_URL + str(ctr) + "/ancestry")

    # badges = ancestry.find('div', class_="card-body d-flex flex-column justify-content-center").find_all('span', class_="badge badge-soft-success fs--2")
    # names = ancestry.find_all('a', class_="font-sans-serif lh-1 fs-2 mb-1 me-2")
    # try:
    #     class_num = badges[0].text.strip().split(" (")[0]
    #     name = names[0].text.strip()
    #     breed_type = badges[1].text.strip().split(" ")[2]
    #     mother = ""
    #     father = ""
    #     if breed_type != "Genesis":
    #         father = names[1].text.strip()
    #         mother = names[2].text.strip()
    #     horse.class_rank = class_num
    #     horse.name = name
    #     horse.mother = mother
    #     horse.father = father
    #     return horse
    # except Exception:
    #     return None
    return horse
