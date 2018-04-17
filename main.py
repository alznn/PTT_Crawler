import requests
import re
import lxml
from bs4 import BeautifulSoup
import pandas as pd
reg = "</div>.*--"
#<\/div>\n(.*[\S\s]+)\-\-
def output(tmp):
    data = pd.Series(tmp)
    data.columns = ["author", "title", "date", "content"]
    data.to_csv("Movie.csv",mode = 'a', encoding='utf-8', index=False,header=True)


def InfoAndContent(links):
    outFile = []
    for link in links:
        tmp = []
        news_url = "https://www.ptt.cc/" + link
#        news_url = "https://www.ptt.cc/bbs/movie/M.1092719966.A.C44.html"
        print(news_url)
        res = requests.get(news_url)
        soup = BeautifulSoup(res.text.encode('utf-8'), 'lxml')
        main_content = soup.find(id="main-content")
        if str(main_content) == "None":
            print("Hi")
        else:
            metas = main_content.select('div.article-metaline')
            author = metas[0].select('span.article-meta-value')[0].getText()
            title = metas[1].select('span.article-meta-value')[0].getText()
            date = metas[2].select('span.article-meta-value')[0].getText()
            tmp.append(author)
            tmp.append(title)
            tmp.append(date)
            filtered = [v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] and not soup.select('div.class.push')]
            content = ' '.join(filtered)

            content = re.sub(r'(\-\-)+.*', '', content)
            content = re.sub(r'[作者|發信人].+([[1|2]([0-9]{3}))','', content)
            #content = re.sub(r'.+轉信站.+\n', '', content)
            content = re.sub(r'\n','', content)
            tmp.append(content)
            print(author)
            print(title)
            print(date)
            #print("content:\n",content)
            #outFile.append(tmp)
            output(tmp)


# main
links = []

url = 'https://www.ptt.cc/bbs/movie/index.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')
#movie 版 index : 1-6583,""
for i in range(1,3):
    if i == 0:
        url = 'https://www.ptt.cc/bbs/movie/index.html'  #newest
    else:
        url = 'https://www.ptt.cc/bbs/movie/index'+str(i)+'.html'
#    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    articles = soup.find_all('div', 'r-ent')
# #print(articles)
    for article in articles:
        meta = article.find('div', 'title').find('a')
 #       print(meta)
        title = meta.getText().strip(" ")
 #       print(meta)
        link = meta.get('href')
#        print(link)
        links.append(link)

    InfoAndContent(links)