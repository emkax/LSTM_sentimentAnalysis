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

baju = "https://www.tokopedia.com/snapstyle-boutique/kaos-distro-tacion-atasan-retro-lengan-pendek-baju-kaos-pria-wanita-1730283062472050510/review"
vitamin =  "https://www.tokopedia.com/nowfoods/now-foods-vitamin-d-3-1000-iu-180-sgels-1729572978135894440/review"
hp = "https://www.tokopedia.com/ismile-indonesia/apple-iphone-13-garansi-resmi-128gb-256gb-512gb-1733418950115362699/review"
sunscreen = "https://www.tokopedia.com/moell-official/moell-physical-sunscreen-spf-50-pa-broad-spectrum-uva-uvb-perlindungan-maksimal-kulit-anak-skincare-microbiome-teknologi-formulasi-dokter-skincare-bayi-skincare-anak-1732634986041410631/review"
sepatu = "https://www.tokopedia.com/ssstoreid-2/sepatu-adidas-handbal-spezial-ice-blue-sneakers-casual-pria-wanita-original-sneakers-murah-size39-43-ice-blue-39-31bd5/review"
parfum = "https://www.tokopedia.com/guardian-officia/fres-natural-cologne-muse-of-the-day-100ml/review"
tas = "https://www.tokopedia.com/light-gwin-original/light-gwin-seling-bag-tas-wanita-sling-bag-terbaru-2025-3-ruang-bahan-kulit-tas-selempang-wanita-kekinian-gaya-corean-style-1732291777124796232/review"
jam_tangan = "https://www.tokopedia.com/amazfitofficial-/amazfit-official-bip-6-smart-watch-46mmai-voice-assistancemaps-with-gps-140-sports-modeshealth-monitoring-1731200712152286714/review"

baju1 = "https://www.tokopedia.com/jasminefashion46/get-1-pcs-promo-cod-kaos-distro-lengan-pendek-c1235-text-hitam-kaos-pria-dan-wanita-premium-quality-motif-lengan-pendek-terbaru-atasan-combed-high-casual-1730839851637048968/review"
baju2 = "https://www.tokopedia.com/fashion-good-t-shiet/t-shirt-rucas-ldistro-pria-wanitapremium-black-oblong-baju-polos-kaos-cowok-keren-surfing-atasan-1732245262251296123/review"
baju3 = "https://www.tokopedia.com/berkahfashion89/befa-kemeja-luna-kemeja-wanita-atasan-wanita-stripe-salur-kemeja-basic-lengan-panjang-1731870976840992595/review"

kecantikan1 = "https://www.tokopedia.com/cetaphil/cetaphil-gentle-skin-cleanser-1000ml-dengan-niacinamide-glycerin-dan-panthenol-sabun-pembersih-muka-untuk-segala-jenis-kulit-1729612968774830812/review"
kecantikan2 = "https://www.tokopedia.com/glowcircle-432/kahf-face-wash-100ml-sabun-wajah-pria-triple-action-oil-comedo-defense-acne-gentle-exfoliating-scrub-hitam-coffee-mencerahkan-membersihkan-muka-cleansing-facial-cowok-1730502059174233141/review"


parfum1 = "https://www.tokopedia.com/scarlettwhite/scarlett-eau-de-parfum-extrait-de-parfum-30ml-wangi-tahan-lama-wangi-mewah-1732312928676578680/review"


body_wash1 = "https://www.tokopedia.com/amorens/amorens-body-wash-bpom-1000ml-sabun-mandi-jumbo-melembabkan-kulit-dan-menutrisi-kulit-soft-rose-berry-bloom-fresh-flower-fresh-coffee-blue-floral-natural-jasmine-1729715658150151736/review"
body_wash2 = "https://www.tokopedia.com/watsons-indonesia-official-store/k-natural-bodywash-w-sparkling-magnolia-pouch-400ml-1730097898368501017/review"

celana1 = "https://www.tokopedia.com/king-pants/celana-kantor-formal-pria-slimfit-premium-hitam-panjang-kerja-kain-lembut-nyaman-katun-bahan-wool-tidak-mudah-berbulu-navy-abu-chino-1729668277208647633/review"
celana2 = "https://www.tokopedia.com/ryl-outfitt/m-xxl-celana-panjang-elegant-pria-dewasa-celana-sam-premium-trousers-stretch-twill-katun-chino-casual-hitam-formal-kerja-distro-kantor-santai-keren-sweatpants-baggy-eclipse-celana-kalcer-straight-pants-1729666110575248468/review"

jaket1= "https://www.tokopedia.com/bgsd-shop/jaket-gorpcore-anti-air-waterproof-simple-keren-nagoya-supply-pria-dan-wanita-distro-parasut-1729980324952704974/review"
links = [body_wash2]

def get_rating(sel_art):
    """Get rating from one <article> element (Selenium)."""
    try:
        rating_elem = sel_art.find_element(By.XPATH, './div/div[1]/div/div')
        aria = rating_elem.get_attribute("aria-label") or ""
        m = re.search(r"\d+(\.\d+)?", aria)
        return float(m.group()) if m else None
    except Exception:
        return None


def get_comment(sel_art, driver):
    """
    Click 'read more' button inside this article (if any),
    then parse the article's HTML with BS4 and extract the comment text.
    """
    # 1. Try expand comment
    try:
        btn = sel_art.find_element(By.XPATH, './/div/p/button')
        driver.execute_script("arguments[0].click();", btn)
        print("EXPANDED")
        time.sleep(0.2)  # give DOM a moment to update
    except NoSuchElementException:
        # no "read more" button → comment already fully visible
        pass

    # 2. Get updated HTML for THIS article only
    html = sel_art.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")

    # 3. Find the comment span
    comment_block = soup.select_one("div.css-1k41fl7 p span")
    return comment_block.get_text(strip=True) if comment_block else None


def main(driver, writer):
    # loop halaman
    count = 0
    while True:
        # Tunggu review muncul
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#review-feed article"))
        )

        # Scroll untuk load data tambahan
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(2)

        # Ambil semua article dengan Selenium (rating + comment)
        selenium_articles = driver.find_elements(By.XPATH, '//*[@id="review-feed"]/article')

        comments = []

        for sel_art in selenium_articles:
            data = {}
            data["rating"] = get_rating(sel_art)
            data["comment"] = get_comment(sel_art, driver)
            if data["comment"] is not None:
                comments.append(data)

        print(comments)

        # Tulis ke CSV
        writer.writerows(comments)

        # Coba klik tombol "next page"
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

            # jika tidak disable → klik next
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(1)
        except Exception:
            print("button disabled or not found, stopping pagination")
            break

        count += 1
        print(f"on page {count}")


# === CSV setup (header only once) ===
csv_file = "result.csv"
file_exists = os.path.isfile(csv_file)

with open(csv_file, "a", newline="", encoding="utf-8") as f:
    fieldnames = ["rating", "comment"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    # scrape all links
    for link in links:
        driver = webdriver.Chrome()
        driver.get(link)
        print(f"Scraping: {link}")
        main(driver, writer)
        driver.quit()

print("Done.")
