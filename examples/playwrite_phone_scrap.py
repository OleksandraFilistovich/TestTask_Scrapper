from playwright.sync_api import sync_playwright


def scrape_webpage(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        button = page.get_by_role("link").get_by_text("показати")
        button.nth(0).click()

        phone_number = page.query_selector('.popup-successful-call-desk')
        print(phone_number.text_content())

        browser.close()

if __name__ == "__main__":
    url = "https://auto.ria.com/uk/auto_audi_e_tron_34759272.html"
    scrape_webpage(url)
