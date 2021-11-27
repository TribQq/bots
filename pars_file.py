import requests
from bs4 import BeautifulSoup

class Parse:
    """main pars"""
    def __init__(self):
        self.list_dict_riddle = []
        self.HEADERS = {     #self. mb
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64;  x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'accept': '*/*'}  # адрес браузера , которкое значение аццепта
        self.URL = 'https://www.braingle.com/brainteasers/category.php?category=All&fields=&value=&unrated=0&order=3&dir=0&start=' # const
        self.page_riddle_counter = 0

    def get_html(self, url_page, params = None):
        r = requests.get(url_page , headers = self.HEADERS , params = params)
        return r

    def pars_main_get_riddle_page_1(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('td', class_='nowrap col_max')  # итемы загадок
        # print('взял список ссылок на ')
        for item in items:
            self.pars_main_get_riddle_page_2(item)
        self.next_page()

    def pars_main_get_riddle_page_2(self,item):
        href_for_riddle = 'https://www.braingle.com/' + item.find('a').get(
            'href')  # кусочек адреса 1 + кусочек 2 (1 статичен, 2й достаём из хтмля
        # if self.get_html(href_for_riddle) == 200: #подмоть надо вай донт ворк
        self.pars_riddle_page(href_for_riddle)
        # print(href_for_riddle) # ссылка на загадку(мб её тоже в дикт?)

    def pars_riddle_page(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all( id = 'main_content')
        for item in items:
            riddle_name = item.find('h1').get_text()
            riddle_body = item.find_all(class_ = 'textblock')
            riddle_text,riddle_answer = riddle_body[0].get_text(),riddle_body[1].get_text()
            dict_riddle={'riddle name : ':riddle_name ,'riddle text : ':riddle_text , 'riddle answer : ':riddle_answer}
            self.list_dict_riddle.append(dict_riddle)


    def next_page(self):
        # print('NEXT PAGE')
        self.page_riddle_counter += 15
        if self.page_riddle_counter <= 15:
            # print(self.page_riddle_counter)# принт каунтера страницы
            self.parse_page()
        else:
            # print(self.list_dict_riddle)
            print('всего распараршено загадок : ' , self.page_riddle_counter)

    def parse_page(self):
        url = self.URL + str(self.page_riddle_counter)
        html = self.get_html(url)
        if html.status_code == 200 :
            self.pars_main_get_riddle_page_1(html.text)
        else:
            print(' Error ')

if __name__ == '__main__':
    print()
    tst=Parse()
    tst.parse_page()
    for dict in tst.list_dict_riddle:
        print(dict)