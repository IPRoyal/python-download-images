import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# fetch the HTML page
page_url = "https://books.toscrape.com/"
res = requests.get(page_url)
soup = BeautifulSoup(res.text, "html.parser")

# extract all <img> tags
img_tags = soup.find_all("img")

# Loop through and download each image
for img in img_tags:
    img_url = img.get("src")  # may be relative
    full_url = urljoin(page_url, img_url)  # make absolute

    # download images
    img_res = requests.get(full_url)
    
    # create a file name from the URL
    file_name = full_url.split("/")[-1]

    with open(file_name, "wb") as f:
        f.write(img_res.content)