import requests
from bs4 import BeautifulSoup as tang

class book():
    def __init__(self):
        self.url = "https://www.biquqq.com/0_1/1.html"
        self.useragent = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    
    def getdata(self, url):
        response = requests.get(url,headers=self.useragent)
        response.encoding = 'utf-8'
        return response.content
    
    def gettitle(self, response):
        soup = tang(response, "html.parser")
        title = soup.find('div', class_='bookname')
        title = title.h1.text
        return title
    
    def getcontent(self, response):
        soup = tang(response, "html.parser")
        content = soup.find('div', id = 'content')
        return content.text
    
    def writefile(self, title, content):
        with open(title + '.txt', 'w') as f:
            f.write(content)
        
if __name__ == "__main__":
    book = book()
    title = book.gettitle(book.getdata(book.url))
    content = book.getcontent(book.getdata(book.url))
    book.writefile(title,content)
