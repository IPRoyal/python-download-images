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