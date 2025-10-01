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