import requests
import wget
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# fetch the HTML page
page_url = "https://books.toscrape.com/"
res = requests.get(page_url)
soup = BeautifulSoup(res.text, "html.parser")

# extract all <img> tags
img_tags = soup.find_all("img")

# loop through and download image
for img in img_tags:
    img_url = img.get("src")
    full_url = urljoin(page_url, img_url)  # make absolute

    # download directly to file
    wget.download(full_url, out=full_url.split("/")[-1])
    print(f"Downloaded {full_url.split('/')[-1]}")