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
    plays = []
    for url in urls:
        print('Downloading', url)
        quotes = []
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text)
        first = soup.find('blockquote')
        if first:
            for tag in first.parent():
                if 'name' in tag.attrs:
                    print(tag.attrs)
                    quotes.append(tag.get_text().strip())
        if quotes:
            plays.append(quotes)
    return plays
if __name__ == '__main__':
    DATA = download()
    with open('shakespeare.json', 'w') as file:
        json.dump(DATA, file)
