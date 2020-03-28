import  pyodbc
from bs4 import BeautifulSoup
import  requests
#爬取猫眼电影TOP100 保存到SQL Servver数据库
db= pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-TAQHEM0\SQLEXPRESS;DATABASE=python;UID=******;PWD=******')
cursor=db.cursor();
cursor.execute("""CREATE TABLE movies
(
电影 varchar(255),
演员 varchar(255),
上映时间 varchar(255),
评分 varchar(255),
详情 varchar(255),
图片地址 varchar(255)
);""")
db.commit()

page =0
url="https://maoyan.com/board/4?offset="
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
for page in range(0,100,10):
    url_r= url + str(page)
    r=requests.get(url_r,  headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    movies = soup.find_all('dd')
    for movie in movies:
        name = movie.find('p', class_='name').find('a').text
        actor = movie.find('p', class_='star').text.strip()
        releasetime = movie.find('p', class_='releasetime').text
        score = movie.find('i', class_='integer').text + movie.find('i', class_='fraction').text
        img_url = movie.find('img', class_='board-img')['data-src']
        info_url = 'https://maoyan.com' + movie.find('p', class_='name').find('a')['href']
        sql="INSERT INTO movies(电影, 演员, 上映时间,评分,详情,图片地址) VALUES('%s','%s','%s','%s','%s','%s')"
        date=(name,actor,releasetime,score,info_url,info_url)
        cursor.execute(sql % date)
        db.commit()


db.close()