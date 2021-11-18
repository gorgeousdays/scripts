# coding=utf-8
"""
Module Summary Here.
Get article from soft.zjut.edu.cn
Authors: gorgeousdays@outlook.com
Create time:2021.11.18
"""
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

url="http://www.soft.zjut.edu.cn/index!sonlist.do?id=24&currentPage="
url_begin="http://www.soft.zjut.edu.cn/"
folder_path="D:\\softzjut\\"


def mkdir(path):
    try:
        folder = os.path.exists(path)
        os.makedirs(path)
    except BaseException:
        pass

def check(name):
    return name.replace('\\', ' ').replace('/', ' ').replace(':', ' ').replace('*', ' ').replace('?', ' ').replace('<', ' ').replace('>', ' ').replace('|', ' ').replace('"', ' ')

def save(content, article_title):
    save_name = folder_path  + check(article_title) + '.html'
    with open(save_name, 'w', encoding='utf-8') as f:
        f.write(content)


def getArticleLinkFromPage(page_url):
    session = requests.session()
    response = session.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    articles = soup.findAll(name="div", attrs={"class" :"list_news"})[0].findAll('a')
    for article in articles:
        article_link= url_begin+str(article).split()[1][6:-1]
        article_title = re.findall(r'>(.*?)<', str(article))[0]
        response = session.get(article_link)
        article_content=response.text
        print(article_title)
        save(article_content,article_title)


def main(start_page,end_page):
    for page in tqdm(range(start_page, end_page+ 1)):
        new_url=url+str(page)
        print("---------The "+str(page)+" Pgae--------")
        getArticleLinkFromPage(new_url)


if __name__ == '__main__':
    main(start_page=1,end_page=2)