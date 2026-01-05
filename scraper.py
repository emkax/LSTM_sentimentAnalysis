from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time
import csv
import os


with open("link_toko.txt",'r') as f:
    links = [line.strip() for line in f if line.strip()]

def get_rating(sel_art):
    try:
        rating_elem = sel_art.find_element(By.XPATH, './div/div[1]/div/div')
        aria = rating_elem.get_attribute("aria-label") or ""
        m = re.search(r"\d+(\.\d+)?", aria)
        return float(m.group()) if m else None
    except Exception:
        return None


def get_comment(sel_art, driver):
    # expand comment
    try:
        btn = sel_art.find_element(By.XPATH, './/div/p/button')
        driver.execute_script("arguments[0].click();", btn)
        print("EXPANDED")
        time.sleep(0.2)
    except NoSuchElementException:
        pass

    html = sel_art.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")

    # letak span comment
    comment_block = soup.select_one("div.css-1k41fl7 p span")
    return comment_block.get_text(strip=True) if comment_block else None


def main(driver, writer):
    count = 0
    while True:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#review-feed article"))
        )

        # scroll untuk load data tambahan
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(2)

        # rating + comment
        selenium_articles = driver.find_elements(By.XPATH, '//*[@id="review-feed"]/article')

        comments = []

        for sel_art in selenium_articles:
            data = {}
            data["rating"] = get_rating(sel_art)
            data["comment"] = get_comment(sel_art, driver)
            if data["comment"] is not None and len(data['comment']) >= 5:
                comments.append(data)

        print(comments)

        writer.writerows(comments)

        try:
            next_button = driver.find_element(
                By.XPATH,
                '//*[@id="zeus-root"]/div/main/div[2]/div[1]/div/section/div[3]/nav/ul/li[11]/button'
            )

            disabled_attr = next_button.get_attribute("disabled")
            aria_disabled = next_button.get_attribute("aria-disabled")
            class_attr = next_button.get_attribute("class") or ""

            if disabled_attr is not None or aria_disabled == "true" or "disabled" in class_attr:
                print("NEXT BUTTON DISABLED – STOP PAGINATION")
                break

            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(1)
        except Exception:
            print("button disabled or not found, stopping pagination")
            break

        count += 1
        print(f"on page {count}")



csv_file = "result.csv"
file_exists = os.path.isfile(csv_file)

with open(csv_file, "a", newline="", encoding="utf-8") as f:
    fieldnames = ["comment","rating"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    for link in links:
        driver = webdriver.Chrome()
        driver.get(link)
        print(f"Scraping: {link}")
        main(driver, writer)
        driver.quit()

print("Done.")
