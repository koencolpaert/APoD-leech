import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

site = 'https://apod.nasa.gov/apod/astropix.html'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]

for url in urls:
    filename = re.search(r'([\w_-]+[.](jpg|gif|png))$', url)
    filename = re.sub(r'\d{4,}\.', '.', filename.group(0))

    with open(filename, 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            hostname = urlparse(site).hostname
            scheme = urlparse(site).scheme
            url = '{}://{}/{}'.format(scheme, hostname, url)

        # for full resolution image the last four digits needs to be striped
        url = re.sub(r'\d{4,}\.', '.', url)

        print('Fetching image from {} to {}'.format(url, filename))
        response = requests.get(url)
        f.write(response.content)
