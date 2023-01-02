import requests
from bs4 import BeautifulSoup

url = 'https://www.biquqq.com/0_1/1.html'

req = requests.get(url)

req.encoding = 'gbk'

soup = BeautifulSoup(req.text,"html.parser")

print(soup.title.text)