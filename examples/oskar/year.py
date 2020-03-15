import time
import pandas as pd
from collect import Collect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pipeline.tasks import Task, join, sleep

URL = "https://reg.goteborgsvarvet.se/sok/resultatlista.aspx"
TAB_RESULT = "//*[@id='tabs']/li[3]/a"
INPUT_YEAR = "//*[@id='MainSection_lYear']"
INPUT_RACE = "//*[@id='MainSection_lRace']"
SUBMIT_FILTER = "//input[@id='listfilter']"
ANCHOR_RUNNER = "//a[contains(@id, 'MainSection_resultListRepeater_nameLink')]"
BTN_NEXT = "//a[@id='MainSection_next']"
TABLE_TITLE = "//*[@id='MainSection_resultListUpdatePanel']/div[2]/div[1]"


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10)

    return driver


async def navigate_to_results(driver, year):
    driver.get(URL)

    driver.find_element_by_xpath(TAB_RESULT).click()

    # set year
    select = Select(driver.find_element_by_xpath(INPUT_YEAR))
    select.select_by_value(year)

    # set race
    select = Select(driver.find_element_by_xpath(INPUT_RACE))
    select.select_by_visible_text("Göteborgsvarvet " + year)

    # apply filter
    await sleep(2)
    filterbtn = driver.find_element_by_xpath(SUBMIT_FILTER)
    filterbtn.click()

    return driver


def get_runner_urls(driver):
    # find runner href urls in list
    elements = driver.find_elements_by_xpath(ANCHOR_RUNNER)
    urls = [e.get_attribute("href") for e in elements]

    return urls


class ScrapeYear(Task):
    async def run(self, year, **inputs):
        year = str(year)
        driver = init_driver()                      # setup selenium web driver (chrome)
        driver = await navigate_to_results(driver, year)  # go to result list

        urls = []
        subtasks = []
        old_title = driver.find_element_by_xpath(TABLE_TITLE).text

        while True:
            print("Collecting for", old_title)
            urls += get_runner_urls(driver)

            if len(urls) >= 1000:
                subtasks.append(self.spawn(Collect, year=year, urls=urls))

                urls = []

            nextbtn = driver.find_element_by_xpath(BTN_NEXT)
            driver.execute_script("arguments[0].click();", nextbtn)

            if "disabled" in nextbtn.get_attribute("class"):
                break

            # Make sure the new page with a new table has loaded
            while True:
                try:
                    title = driver.find_element_by_xpath(TABLE_TITLE).text
                    assert old_title != title
                    old_title = title
                    break
                except:
                    await sleep(1)
            break
        
        if len(urls) > 0:
            subtasks.append(self.spawn(Collect, year=year, urls=urls))  # remaining urls

        driver.close()          # close selenium driver
        await join(*subtasks)   # wait for all background jobs to complete

        return {
            'Finished': year
        }
