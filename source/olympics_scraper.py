from selenium import webdriver
# -*- coding: UTF-8 -*-
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


class OlympicsAthletesScraper():
    """Scraper of Athletes in https://olympics.com/es/atletas/"""
    def __init__(self):
        """Scraper creation"""
        # URL and search configuration
        self.url = "https://www.olympiandatabase.com/index.php?id=44926&L=1"

        # class variables
        self.driver_options = None
        self.driver = None
        self.wait = None
        self.data_info = None
        self.last_link = None

        # create random generator method of numbers between 0 and 1
        rng = np.random.default_rng()
        self.random = rng.random

    def __configure_webdriver_options(self):
        """Configuration of driver before creating driver to prevent selenium detection"""
        options = webdriver.ChromeOptions()
        # initialize maximizing
        options.add_argument("start-maximized")

        # disable the Automation Controlled flag
        options.add_argument("--disable-blink-features=AutomationControlled")

        # exclude the collection of enable-automation switches
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # disable useAtomationExtension
        options.add_experimental_option('useAutomationExtension', False)
        self.driver_options = options

        return

    def init_driver(self):
        """Init driver. Driver options are configured to prevent selenium detection.
        UserAgent is Override to the standard in the browser"""
        # configure driver options
        self.__configure_webdriver_options()

        # start driver
        driver = webdriver.Chrome(options=self.driver_options)

        # change property of the navigator value for webdriver to undefined
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # override user-agent and shows user agent
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

        self.driver = driver
        # show progress of the process
        print('Driver started. userAgent:')
        print(driver.execute_script("return navigator.userAgent;"))

        # create wrapper for WebDriverWait
        self.wait = WebDriverWait(driver, 15)
        return

    def start_scraping_session(self, url, accept_cookies=False):
        """
        Start navigation in the url and do a search for the specific job profile and location
        """
        # init variables
        driver = self.driver
        wait = self.wait

        # get url
        self.url = url
        driver.get(self.url)

        # sleep time before to mimic human behaviour
        time.sleep(2.5 + self.random())

        if accept_cookies:
            # accept cookies
            cookies_ok_btn = EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.cc_btn.cc_btn_accept_all'))
            wait.until(cookies_ok_btn).click()
            time.sleep(self.random())

        return

    def find_links_in_page(self, ):
        driver = self.driver

        # find links in competition
        links_in_comp = driver.find_elements(by=By.CSS_SELECTOR, value="td [href]")
        links_in_comp_raw = []

        # skip top_row_of links
        k_to_skip = 0
        for k, link_el_c in enumerate(links_in_comp):
            # stop condition
            stop_c = link_el_c.text.strip().lower() == 'schedule'
            stop_c |= link_el_c.text.strip().lower() == 'history'

            if stop_c:
                k_to_skip = k

        # loop rest of links
        links_list = []
        for link_el_c in links_in_comp[k_to_skip + 1:]:
            # stop condition
            stop_c = link_el_c.text == 'Olympian Database'
            stop_c |= link_el_c.text.strip() == 'All-time Medal Table'
            if stop_c:
                break
            # ckeck is blank
            if link_el_c.text.strip() == '':
                pass
            else:
                link = link_el_c.get_attribute('href')
                if link not in links_list:
                    links_in_comp_raw.append((link_el_c.text, link))
                    links_list.append(link)

        return links_in_comp_raw

    def extract_individual_participants(self, season, city, year, sport_name, c_name):

        driver = self.driver
        # find rows
        rows = driver.find_elements(by=By.CSS_SELECTOR, value="tr")

        # init out list
        out_l = []
        old_country = None

        # loop in rows
        for row in rows:
            # find td elements and filter when there are six
            td_els = row.find_elements(by=By.CSS_SELECTOR, value="td")
            if len(td_els) == 7:
                if len(td_els[3].text) == 3:
                    new_country = td_els[3].text
                else:
                    new_country = old_country

                vals = (season, city, year,
                        sport_name, c_name, td_els[1].text, new_country)

                old_country = new_country
                if vals not in out_l:
                    out_l.append(vals)

        return out_l

    def extract_team_participants(self, n_participants, season, city, year, sport_name, c_name):
        driver = self.driver
        # find rows
        rows = driver.find_elements(by=By.CSS_SELECTOR, value="tr")

        # init out list
        out_l = []
        country_done = []

        # loop in rows
        for row in rows:
            # find td elements and filter when there are six
            td_els = row.find_elements(by=By.CSS_SELECTOR, value="td")
            if len(td_els) == 10:
                country_1 = td_els[1].text
                country_2 = td_els[4].text
                if (len(country_1) == 3) & (len(country_2) == 3):
                    new_countries = [country_1, country_2]

                    for new_c in new_countries:
                        if new_c not in country_done:
                            country_done.append(new_c)
                            for k in range(n_participants):
                                vals = (season, city, year,
                                        sport_name, c_name, '{}_{}'.format(c_name, k + 1), new_c)

                                if vals not in out_l:
                                    out_l.append(vals)

        return out_l

    def extract_individual_competition(self, sport_name, link, all_athletes, season, city, year):
        """Process individual competitions"""
        driver = self.driver

        # get link
        driver.get(link)
        time.sleep(0.2 + self.random())

        # find links in competition
        links_in_comp_raw = self.find_links_in_page()

        for link_in_comp_raw in links_in_comp_raw:

            c_name = link_in_comp_raw[0]
            link = link_in_comp_raw[1]
            print('\rExtracting {} - {}'.format(sport_name, c_name), end='')

            # get link
            driver.get(link)
            time.sleep(0.2 + self.random())

            out_l = self.extract_individual_participants(season, city, year, sport_name, c_name)

            if len(out_l) == 0:
                print('\rError: {} - {}'.format(sport_name, c_name))
            all_athletes += out_l

        return all_athletes

    def extract_team_sport(self, sport_name, link, all_athletes, season, city, year):
        """Process team competitions"""
        driver = self.driver

        # get link
        driver.get(link)
        time.sleep(0.2 + self.random())

        # find links in competition
        links_in_comp_raw = self.find_links_in_page()

        # find rows to identify team of winner
        competition_names = [x[0] for x in links_in_comp_raw]
        competition_links = [x[1] for x in links_in_comp_raw]

        competition_participants = []
        rows = driver.find_elements(by=By.CSS_SELECTOR, value="tr")
        # identify elements in rows
        n_participants = None
        for k, row in enumerate(rows[5:]):
            tds = row.find_elements(by=By.CSS_SELECTOR, value="td")
            if tds[0].text in competition_names:
                if n_participants is not None:
                    competition_participants.append(n_participants)

                n_participants = 1

            elif 'Olympian Database' in tds[0].text:
                break
            elif 'All-time Medal Table' in tds[0].text:
                break
            else:
                if len(tds) >= 4:
                    if tds[4].text.strip() != '':
                        n_participants += 1

        if n_participants is not None:
            competition_participants.append(n_participants)

        for c_name, link, n_participants in zip(competition_names, competition_links, competition_participants):

            print('\rExtracting {} - {}'.format(sport_name, c_name), end='')

            # get link
            driver.get(link)
            time.sleep(0.2 + self.random())

            # Exception Volleyball - Beach volley
            team_as_individuals = [('Volleyball', 'Beach volley')]
            is_exception = any([(x[0] in sport_name) and (x[1] in c_name) for x in team_as_individuals])
            if is_exception:
                out_l = self.extract_individual_participants(season, city, year, sport_name, c_name)
            else:
                out_l = self.extract_team_participants(n_participants, season, city, year, sport_name, c_name)

            if len(out_l) == 0:
                print('\rError: {} - {}'.format(sport_name, c_name))
            all_athletes += out_l

        return all_athletes

    def find_athletes(self,  season, city, year):
        """Process athlete name"""
        # init variables
        driver = self.driver
        wait = self.wait
        all_athletes = []
        team_sports = ['Baseball', 'Basketball', 'Football', 'Handball', 'Hockey',
                       'Rugby', 'Softball', 'Volleyball', 'Water Polo',
                       'Ice Hockey', 'Curling']

        # find links in competition
        link_elements_raw = self.find_links_in_page()

        # loop elements in sports
        for link_el_raw in link_elements_raw:
            sport_name = link_el_raw[0]
            link = link_el_raw[1]

            # exception Curling 2018
            if sport_name == 'Curling' and year == '2018':
                all_athletes = self.extract_individual_competition(sport_name, link, all_athletes,
                                                                   season, city, year)
            elif sport_name in team_sports:
                all_athletes = self.extract_team_sport(sport_name, link, all_athletes,
                                                       season, city, year)
            else:
                all_athletes = self.extract_individual_competition(sport_name, link, all_athletes,
                                                                   season, city, year)
        return all_athletes

