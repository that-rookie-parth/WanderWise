from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

# chrome_options = Options()
# # chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_driver_path = "./chromedriver"
browser = webdriver.Chrome()


def get_data(link: str):
    browser.get(link)
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    content = soup.text
    text = content.split("\n")
    text = list(filter(lambda x: len(x.strip()) > 0, text))
    return "\n".join(text)


def main():
    list_of_links = [
        "https://www.incredibleindia.org/content/incredible-india-v2/en/destinations/states/maharashtra.html",
        "https://www.incredibleindia.org/content/incredible-india-v2/en/destinations/states/tamil-nadu.html",
        "https://www.incredibleindia.org/content/incredible-india-v2/en/destinations/states/uttar-pradesh.html"
    ]
    for i, link in tqdm(enumerate(list_of_links)):
        content = get_data(link)
        with open(f"./scraped_content/content-{i}.txt", "w") as f:
            f.write(content)


if __name__ == "__main__":
    main()
    browser.quit()