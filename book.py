import requests
from bs4 import BeautifulSoup
url = "http://www.ltoooo.com/"
searchUrl = "http://www.ltoooo.com/s.php?ie=gbk&q="
def get_book_list():
    # 搜索书名
    name = input("请输入书名：")
    listUrl = searchUrl + name
    strhtml = requests.get(listUrl)
    soup=BeautifulSoup(strhtml.text,'lxml')
    data = soup.select('body > div.wrap > div > div > div > div > div.bookinfo > h4 > a')
    # 判断是否有搜索结果
    if(len(data)!=0):
      # 选择搜索结果
      for index,item in enumerate(data):
        print(index+1,item.get_text())
      b_index = int(input("请输入对应的书名序号："))
      book_code = data[b_index - 1].get('href')
      # 爬取对应章节
      booklist = requests.get(url+book_code)
      booksoup=BeautifulSoup(booklist.text,'lxml')
      result = booksoup.select("body > div.listmain > dl > dd > a")
      for i,c in enumerate(result):
        print(i+1,c.get_text())

      type = int(input("请选择爬取的类型？（1.单篇阅读 2.全部保存）："))

      if(type==1):
        #1.用户选择单篇阅读
        # 获取对应的章节code
        chapter_index = int(input("请输入您想观看的章节序号："))
        get_chapter(chapter_index,result,data,b_index)
      else:
        #2.全部保存到text文件中
        get_chapter('',result,data,b_index)

def get_chapter(index,result,data,b_index):
  if(index):
    print('爬取单个章节')
    chapter_code = result[index - 1].get('href')
    # 爬取章节对应文章内容
    chapter_html = requests.get(url+chapter_code)
    chapter_soup=BeautifulSoup(chapter_html.text,'lxml')
    content_data = chapter_soup.select("#content")
    print(content_data[0].get_text())
  else:
    book_name = data[b_index - 1].get_text()
    path = book_name+'.txt'
    for i,c in enumerate(result):
      i_code = result[i].get('href')
      html = requests.get(url+i_code)
      html_s=BeautifulSoup(html.text,'lxml')
      html_data = html_s.select("#content")
      # 写入文件 
      fs = open(path,'a+',encoding="utf-8")
      fs.write(html_data[0].get_text())
      print("当前进度：",str(round(i / (len(result) / 100),2)) + '%')

    print('写入完成')

get_book_list()