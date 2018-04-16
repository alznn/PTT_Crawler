import requests
import re
import lxml
from bs4 import BeautifulSoup
reg = "</div>.*--"
#<\/div>\n(.*[\S\s]+)\-\-
def output(author,title,date,content,table):
    print(author,"\n",title,"\n",date,"\n",content,"\n",table)

def InfoAndContent(links):
    contenUrl = "https://www.ptt.cc/bbs/movie/"
    i = 0
    user = []
    context = []
    for link in links:
#        news_url = "https://www.ptt.cc/" + link
        print(links[0])
        tmp = []
        res = requests.get(links[0])
        soup = BeautifulSoup(res.text.encode('utf-8'), 'lxml')
        main_content = soup.find(id="main-content")
        metas = main_content.select('div.article-metaline')
        author = metas[0].select('span.article-meta-value')[0].getText()
        title = metas[1].select('span.article-meta-value')[0].getText()
        date = metas[2].select('span.article-meta-value')[0].getText()
        tmp.append(author)
        tmp.append(title)
        tmp.append(date)
        filtered = [v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] and not soup.select('div.class.push')]
        ##filtered = [_f for _f in filtered if _f]
        content = ' '.join(filtered)
#        content = re.sub(r'(\s)+', '', content)

        content = re.sub(r'(\-\-)+.*', '', content)
        content = re.sub(r'作者.+\n','', content)
        content = re.sub(r'\n','', content)
        #tmp.append(content)
        #tmp.append("movie")
#        print(author)
#        print(title)
#        print(date)
        print("content:\n",content)
        #output(author,title,date,content,"movie")
# main
links = []

url = 'https://www.ptt.cc/bbs/movie/index.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')
#movie 版 index : 1-6583,""
for i in range(2,3):
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
 #       print(link)
        links.append("https://www.ptt.cc/bbs/movie/M.1089252949.A.35A.html")

    InfoAndContent(links)