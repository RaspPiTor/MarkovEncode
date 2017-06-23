import json
import requests
import bs4


def get_urls():
    base_url = 'http://shakespeare.mit.edu/{name}/full.html'
    req = requests.get('http://shakespeare.mit.edu/')
    soup = bs4.BeautifulSoup(req.text)
    urls = []
    for url in [i.attrs['href'] for i in soup.find_all('a')]:
        if url.endswith('/index.html'):
            name = url.rstrip('/index.html')
            urls.append(base_url.format(name=name))
    return urls


def download():
    urls = get_urls()
    quotes = []
    for url in urls:
        print('Downloading', url)
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text)
        for tag in soup.find_all('blockquote'):
            quotes.append(tag.get_text().strip())
    return quotes
if __name__ == '__main__':
    DATA = download()
    with open('shakespeare.json', 'w') as file:
        json.dump(DATA, file)
