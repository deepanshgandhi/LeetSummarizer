from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_problem_description(url):
    # Initialize the WebDriver (Make sure to specify the path to your WebDriver)
    driver = webdriver.Chrome(executable_path='Scraping/driver/chromedriver')  
    try:
        driver.get(url)
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, "initial-loading")))

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # Adjust the attributes to match the actual HTML structure
        # attr = {"class": "elfjS"}
        # attr = {"class": "content__u3I1 question-content__JfgR"}
        # attr = {"data-track-load": "description_content"}
        description_div = soup.find_all("meta", {"name": "description"})
        if description_div:
            description = description_div
        else:
            description = "Description not found"

        return description

    finally:
        driver.quit()

# Example usage:
url = 'https://leetcode.com/problems/two-sum/'
description = get_problem_description(url)
print(description)
