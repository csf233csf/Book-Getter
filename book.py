import requests
from bs4 import BeautifulSoup as tang
import time
import os.path
import random

class book():
    def __init__(self):
        self.first_url = "https://www.biquqq.com/0_1/3002.html" # For testing 
        self.book_url = "https://www.biquqq.com/0_1/" # Change this url to the book you want to get from 'https://www.biquqq.com'
        self.useragent = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"} # User-Agent that is used
        self.url_root = "https://www.biquqq.com" 
        self.error_count = 0 
        
    def get_response(self, url):
        response = requests.get(url,headers=self.useragent)
        response.encoding = 'utf-8' # changed the html encoding to 'utf-8' because of Chinese characters
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
        try:
            with open(os.path.join('/bookgetter/bookfolder',title + '.txt'), 'w', encoding = 'utf-8') as f:
                f.write(content)
        except OSError: # OsError Exception when the title contains invalid characters to write
            self.error_count += 1
            print("OSError, trying to replace title")
            book.write_file(content.splitlines()[0].strip() ,content) # Writes the title with the first line of that chapter instead
            print("Wrote the file with name: " + content.splitlines()[0].strip())
        except:
            self.error_count += 1
            book.write_file(f"Error File {self.error_count}" ,content) # Recursion
            print(f"Unknown Error, wrote the file with name: 'Error File {self.error_count}'")
    
    def get_chapters(self, response):
        href_list = [] # lists that contain all hrefs 
        chapter_list = [] # chapter url lists
        soup = tang(response, "html.parser")
        listsoup = soup.find('div', id = 'list')
        chapters = listsoup.find_all('a')
        for chap in chapters:
            href_list.append(chap.get('href'))
        for html in href_list[9:]: # The 9 here is to avoid the first 9 href links because the first 9 are preview chapters.
            chapter_list.append(self.url_root + html)
        return chapter_list
    
    def start(self): # loops through chapter list to write, each chapter == 1 text file
        chapter_list = book.get_chapters(book.get_response(book.book_url))
        for chap in chapter_list:
            title = book.get_title(book.get_response(chap))
            content = book.get_content(book.get_response(chap))
            print("Attempt writing: " + title)
            book.write_file(title,content)
            print("Done writing: " + title)
            time.sleep(random.randint(0,3))           

if __name__ == "__main__":
    book = book()
    """title = book.get_title(book.get_response(book.first_url))
    content = book.get_content(book.get_response(book.first_url))
    print(content.splitlines()[0])
    book.write_file(title,content)"""
    # test code block // please ignore
    
    book.start()
    print("Total error occured:", book.error_count)
