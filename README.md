# How to Download Images from URLs with Python

While most developers use libraries like Requests, Urllib3, or Wget for fetching webpage HTML, these tools can also handle image downloads directly from URLs.
Instead of relying on third-party APIs, you can scrape and save images with just a few lines of Python code. This repository shows you how - including proxy support to avoid detection when scraping.

## Downloading Single Image from URL

### Python Requests

The Requests library is the easiest and most reliable way to download images in Python.
- Use requests.get() to fetch the image
- Save the content to a file in binary mode (wb)
- Extract the file name from the URL to keep the correct extension
- Add error handling (try/except) for network and file errors
- Use proxies if you need to scrape at scale

```python
import requests
from requests.exceptions import HTTPError, Timeout, RequestException

def extract_name(url): 
    return url.split("/")[-1]

url = "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"

proxies = {
    "http": "http://user:pass@proxy:port",
    "https": "http://user:pass@proxy:port"
}

try:
    response = requests.get(url, proxies=proxies, timeout=10)
    response.raise_for_status()

    with open(extract_name(url), "wb") as f:
        f.write(response.content)

    print("Image downloaded successfully.")

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")

except Timeout as timeout_err:
    print(f"Request timed out: {timeout_err}")

except RequestException as req_err:
    print(f"Request failed: {req_err}")

except IOError as io_err:
    print(f"File I/O error: {io_err}")
```

### Urllib3

Urllib3 is a lightweight HTTP client for Python, and it’s actually what Requests uses under the hood. You can use it directly to download images with just a few lines of code.
- Always add a timeout to prevent hanging requests
- Use ProxyManager() with make_headers() if your proxy requires authentication
- Save the file using the original name from the URL to keep the correct extension

```python
# Without proxy
import urllib3

url = 'http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg'

res = urllib3.request('GET', url)

def extract_name(url): 
    file_name = url.split("/")[-1]
    return file_name

with open(extract_name(url),'wb') as f:
    f.write(res.data)


# With proxy
import urllib3

default_headers = urllib3.make_headers(proxy_basic_auth='user:pass')
http = urllib3.ProxyManager('http://proxy:port', proxy_headers=default_headers)

url = 'http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg'

res = http.request('GET', url)

def extract_name(url): 
    file_name = url.split("/")[-1]
    return file_name

with open(extract_name(url),'wb') as f:
    f.write(res.data)
```

### Wget

Wget is a simple Python wrapper for the classic Linux wget tool. It’s great for quickly downloading images or files with minimal code.
- Use wget.download(url) with just the target URL.
- By default, the file will be saved with the name taken from the URL.
- Wget does not support proxies.

```python
import wget

# Target image URL
url = "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"

try:
    # Downloads the file and saves it using the original filename from the URL
    filename = wget.download(url)
    print(f"\nImage downloaded successfully: {filename}")
except Exception as e:
    print(f"Error downloading image: {e}")

```

## Downloading Multiple Images from a Website

Instead of direct image URLs, we can scrape a page’s HTML. Using BeautifulSoup, we extract <img> tags and their src attributes. Since some paths are relative, we apply urljoin to build full URLs. Once collected, we loop through the list of image URLs, download each, and save them as files. Below are examples with Requests, Urllib3, and Wget.

### Python Requests

```python
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
```

### Urllib3

```python
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
```

### Wget
The Python Wget library only downloads files and can’t parse HTML for <img> tags. To download multiple images, we pair it with Requests to extract URLs. For simplicity, these snippets omit error handling and proxies, but in real projects you may also need rotating user agents, metadata handling, or custom file naming.

```python
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
```

## Python Libraries for Image Downloading Compared

- Requests - The easiest and most versatile option. Great error handling, built-in proxy support, and widely used in web scraping. Best for most projects.
- Urllib3 -  More control and performance than Requests, but slightly more complex. Suited for advanced users who need fine-tuned networking.
- Wget - Extremely simple for one-off downloads, but limited since it can’t parse HTML or handle proxies natively.

## Conclusion

Downloading images in Python is straightforward with Requests, Urllib3, or Wget. For most developers, Requests is the best all-around choice thanks to its simplicity and ecosystem. Use Urllib3 if you need performance and low-level control, or Wget if you just want quick, no-frills downloads.
