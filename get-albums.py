import re, sys, requests, json
from bs4 import BeautifulSoup

def get_albums(autor):
    urls = f'https://www.letras.com/{autor}/discografia/'
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }

    page = requests.get(urls, headers=headers).content
    page = BeautifulSoup(page, 'html.parser')

    albums = list()
    album_names = page.find_all("div", {"class": ["album-item"]})

    for i in album_names:
        name = i.find_all('h1')[0].get_text()
        name = re.sub('^\s+', '', name)
        name = re.sub('\s+$', '', name)
        year = re.sub('^..(\d+)\s.*$', r'\1', i.find_all('div',{'class':"header-info"})[0].get_text())
        tracks = [ {'track' : y+1, 'song' : x.get_text()} for y, x in enumerate(i.find_all('div', {'class': "song-name"})) ]
        albums.append({'album': name, 'year': year, 'songs': tracks})
    
    return str(albums)


autor = '-'.join(sys.argv[1:])

with open(f"./authors/{autor}.json", "w") as file:
    json.dump(get_albums(autor), file)

