import wget

# Target image URL
url = "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"

try:
    # Downloads the file and saves it using the original filename from the URL
    filename = wget.download(url)
    print(f"\nImage downloaded successfully: {filename}")
except Exception as e:
    print(f"Error downloading image: {e}")
