import requests
from bs4 import BeautifulSoup

# URL = 'https://www.braingle.com/brainteasers/category.php?category=All&fields=&value=&unrated=0&order=3&dir=0&start=0' # const


HEADERS = { 'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64;  x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36' , 'accept' : '*/*' } #адрес браузера , которкое значение аццепта

def get_html(url_page,params = None):
    # в параметрах должен быть пэйдж но в моём случае они измеряют в элементах лол start=45== Page 4
    # , start 40 == page 3, start 0 == page 1 (при этом 45/40/0 не присутс на стр)
    r = requests.get(url_page, headers = HEADERS , params = params)
    return r

def get_content(html ,list_riddle ,step = 2): #работает с данными
    soup = BeautifulSoup(html, 'html.parser') # 2й параметр опционален,желателен , у
    # казывает тип с которым мы работаем(суп может много:))
    items = soup.find_all('td' ,class_ = 'nowrap col_max')
    # if step == 1:  # смена страницы

    if step == 2: # если мы на определённой странице парсим ссылки на загадки
        items = soup.find_all('td', class_='nowrap col_max')
        for item in items:
            riddle_page(item,list_riddle)
        # if

    if step == 3: # парсим загадку
        items = soup.find_all( id = 'main_content')
        for item in items:
            riddle_name = item.find('h1').get_text()
            riddle_body = item.find_all(class_ = 'textblock')
            riddle_text,riddle_answer = riddle_body[0].get_text(),riddle_body[1].get_text()
            dict_riddle={'riddle name : ':riddle_name ,'riddle text : ':riddle_text , 'riddle answer : ':riddle_answer}
            list_riddle.append(dict_riddle)
            #
    return list_riddle




def riddle_page(item,list_riddle):
    href_for_riddle = 'https://www.braingle.com/'+ item.find('a').get('href') # кусочек адреса 1 + кусочек 2 (1 статичен, 2й достаём из хтмля
    parse(list_riddle,3,href_for_riddle)
    # list_riddle.append({ })
    print(href_for_riddle)

def parse(list_riddle, step = 2, url = 'https://www.braingle.com/brainteasers/category.php?category=All&fields=&value=&unrated=0&order=3&dir=0&start=0'):
    html = get_html(url)  # возрващает страницу
    if html.status_code == 200: # если "вэлью == 200( == True) "
        # print(html.text) # отпринтовать страницу в тексте #BeautifulSoup metod
        new_list = get_content(html.text ,list_riddle, step) # пердаём текст
    else:
        print('Error')
    return new_list



if __name__ == '__main__':
    list_riddle = []
    list_dict_riddle = parse(list_riddle)
    print(list_dict_riddle)
    for dict in list_dict_riddle:
        for key,value in dict.items():
            print(key , value)

        print('-'*30)