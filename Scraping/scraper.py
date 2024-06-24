from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver_path = "C:/Users/sanke/Desktop/MLOps/LeetSummarizer/Scraping/driver/chromedriver-win64/chromedriver.exe"
chrome_service = Service(driver_path)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def check_login_status():
    driver.get('https://leetcode.com/')
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-cy="navbar-user-menu"]'))
        )
        print("Logged In!!")
        return True  # Logged in
    except Exception:
        print("Not logged in!!")
        return False  # Not logged in

def fetch_problem_details(problem_url):
    driver.get(problem_url)
    
    # Adding a wait time to let Cloudflare's challenge pass
    time.sleep(10)
    
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cy="question-title"]'))
    )

    title = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="question-title"]').text
    description = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="question-content"]').text

    # Attempt to get the latest code submission
    try:
        code = driver.find_element(By.CSS_SELECTOR, 'div[class*="CodeMirror"]').text
    except Exception as e:
        code = "No code found or unable to locate the code editor"

    problem_id = problem_url.split('/')[-2]
    print(f"Title: {title}\nDescription: {description}\nProblem ID: {problem_id}")
    print(f"Latest Code:\n{code}")

def main():
    if not check_login_status():
        print("User Not Logged in!!!")
    else:
        problem_url = 'https://leetcode.com/problems/two-sum/'
        fetch_problem_details(problem_url)

    driver.quit()

if __name__ == "__main__":
    main()
