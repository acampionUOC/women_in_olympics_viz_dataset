from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
import pandas as pd
import numpy as np
import json
import re
import csv

from source.olympics_scraper import OlympicsAthletesScraper
scraper = OlympicsAthletesScraper()

# step by step execution of the scraper
scraper.init_driver()

out_name = 'athletes_2018_to_2022.csv'
games_to_scrap = [("https://www.olympiandatabase.com/index.php?id=23286&L=1",
                   'Winter', 'PyeongChang', '2018'),

                  ("https://www.olympiandatabase.com/index.php?id=44926&L=1",
                   'Summer', 'Tokyo', '2020'),

                  ("https://www.olympiandatabase.com/index.php?id=109426&L=1",
                   'Winter', 'Beijing', '2022')]

# games_to_scrap = games_to_scrap[1:]
all_athletes = []
for k_g, g in enumerate(games_to_scrap):
    url = g[0]
    season = g[1]
    city = g[2]
    year = g[3]

    scraper.start_scraping_session(url=url, accept_cookies=(k_g == 0))
    game_athletes = scraper.find_athletes(season=season, city=city, year=year)

    all_athletes += game_athletes

df = pd.DataFrame(all_athletes, columns=['Season', 'City', 'Year', 'Sport', 'Event', 'Name', 'NOC'])
df.to_csv(out_name, index=False)

