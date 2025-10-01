import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin

http = urllib3.PoolManager()

# fetch the HTML page
page_url = "https://books.toscrape.com/"
res = http.request('GET', page_url)
soup = BeautifulSoup(res.data, "html.parser")

# Extract all <img> tags
img_tags = soup.find_all("img")

# Loop through and download images
for img in img_tags:
    img_url = img.get("src")
    full_url = urljoin(page_url, img_url)  # make absolute
    
    img_res = http.request('GET', full_url)
    file_name = full_url.split("/")[-1]

    # Save each image
    with open(file_name, "wb") as f:
        f.write(img_res.data)