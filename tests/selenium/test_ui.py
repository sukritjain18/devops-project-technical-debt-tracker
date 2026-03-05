from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_homepage_loads():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get("http://localhost:8080")

    assert "Technical Debt Tracker" in driver.page_source

    driver.quit()