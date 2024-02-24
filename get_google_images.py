import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def get_google_images(query, num_images=20):
    search_query = quote_plus(query)
    url = f"https://www.bing.com/images/search?q={search_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_links = []
    image_containers = soup.find_all("div", {"class": "iuscp"})
    for image_container in image_containers: 
        src = image_container.find("img", {"class": "mimg"})
        text = image_container.find("a", {"class": "inflnk"})
        link = image_container.find("a", {"data-hookid": "pgdom"})
        if text: 
            text = text.get("aria-label")
        else: 
            text = query
        if link: 
            link = link.get("href")
        else: 
            link = ""
        if src: 
            src = src.get("src")
        else: 
            continue
        image_links.append({ "src": src, "text": text, "link": link })
    
    return image_links[:num_images]
