import requests
from bs4 import BeautifulSoup as tang

class book():
    def __init__(self):
        self.first_url = "https://www.biquqq.com/0_1/1.html" # For testing
        self.book_url = "https://www.biquqq.com/0_1/" 
        self.useragent = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
        self.url_root = "https://www.biquqq.com"
    
    def get_response(self, url):
        response = requests.get(url,headers=self.useragent)
        response.encoding = 'utf-8'
        return response.content
    
    def get_title(self, response):
        soup = tang(response, "html.parser")
        title = soup.find('div', class_='bookname')
        title = title.h1.text
        return title
    
    def get_content(self, response):
        soup = tang(response, "html.parser")
        content = soup.find('div', id = 'content')
        return content.text
    
    def write_file(self, title, content):
        with open(title + '.txt', 'w') as f:
            f.write(content)
    
    def get_chapters(self, response):
        href_list = []
        chapter_list = []
        soup = tang(response, "html.parser")
        listsoup = soup.find('div', id = 'list')
        chapters = listsoup.find_all('a')
        for chap in chapters:
            href_list.append(chap.get('href'))
        for html in href_list[9:]: # The 9 here is to avoid the first 9 href links because the first 9 are preview chapters.
            chapter_list.append(self.url_root + html)
        return chapter_list
    
    def start(self):
        chapter_list = book.get_chapters(book.get_response(book.book_url))
        for chap in chapter_list:
            title = book.get_title(book.get_response(chap))
            content = book.get_content(book.get_response(chap))
            book.write_file(title,content)            

if __name__ == "__main__":
    book = book()
    book.start()
    
