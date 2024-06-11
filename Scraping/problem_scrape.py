import os
import json
import re
import requests
import bs4
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from io import BytesIO

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver_path = "Scraping/driver/chromedriver"
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)

PROBLEMSET_BASE_URL = "https://leetcode.com/problemset/all/?page="

def get_html(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Error: Could not get problem page")
        return None
    return r.content

def get_problem_description(url):
    driver.get(url)
    WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, "initial-loading")))
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    description_div = soup.find("div", {"class": "elfjS"})
    # description_div = soup.find("div", {"data-track-load":"description_content"})
    print(soup)
    if description_div:
        description = description_div.get_text(separator='\n')
    else:
        description = "Description not found"
    
    return description

def main():
    problemset = []

    if os.path.exists("Scraping/problemset.json"):
        with open('Scraping/problemset.json', 'r') as f:
            problemset = json.load(f)

    with open('Scraping/problemset.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL", "Acceptance", "Difficulty", "Description"])

        for i in range(1, 2):
            url = PROBLEMSET_BASE_URL + str(i)
            print("processing page: " + url)
            driver.get(url)
            time.sleep(5)
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, "html.parser")
            table = soup.find("div", {"class": "inline-block min-w-full"})
            if not table:
                print("No table found on the page")
                continue
            rowgrp = table.find("div", {"role": "rowgroup"})
            rows = rowgrp.find_all("div", {"role": "row"})
            print(rows)
            for row in rows:
                cells = row.find_all("div", {"role": "cell"})
                if len(cells) < 5:
                    continue
                problem = {}
                problem["title"] = cells[1].text.strip()
                problem["url"] = "https://leetcode.com" + cells[1].find("a")["href"]
                problem["Acceptance"] = cells[3].text.strip()
                problem["difficulty"] = cells[4].text.strip()
                # prints to check cell contents
                print(f"Title: {problem['title']}, URL: {problem['url']}, Acceptance: {problem['Acceptance']}, Difficulty: {problem['difficulty']}")
                try:
                    problem["description"] = get_problem_description(problem["url"])
                except Exception as e:
                    print("Error: Could not get problem page: ", problem["url"], problem["title"], str(e))
                    continue
                # print to check problem details
                print(problem)
                problemset.append(problem)
                writer.writerow([problem["title"], problem["url"], problem["Acceptance"], problem["difficulty"], problem["description"]])

    with open('Scraping/problemset.json', 'w') as f:
        json.dump(problemset, f)

main()



