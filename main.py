import urllib.request,urllib.error
import re
import xlwt
from bs4 import BeautifulSoup


def main():
    print('fucking')
    baseUrl = 'https://movie.douban.com/top250?start='
    filePath = '豆瓣Top250.xls'
    # askUrl(url)
    data = getData(baseUrl)
    saveData(data,filePath)


# 保持数据
def saveData(data,filePath):
    print('saving....')
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('豆瓣Top250',cell_overwrite_ok=True)
    col = ("电影链接","封面链接","电影名","评分","评分人数","电影概况")
    for i in range(len(col)):
        sheet.write(0,i,col[i])
    for i in range(250):
        moiveData = data[i]
        for j in range(len(col)):
            sheet.write(i+1,j,moiveData[j])

    book.save(filePath)




# 循环爬取所有数据
# 豆瓣一页25个电影，共十页
def getData(baseUrl):
    # 电影链接
    findLinkReg = re.compile(r'<a href="(.*?)">')
    # 图片资源
    findImgSrcReg = re.compile(r'<img.*src="(.*?)"',re.S)
    # 电影标题
    findTitleReg = re.compile(r'<span class="title">(.*)</span>')
    # 电影评分
    findRatingReg = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
    # 评价人数
    findJudgeReg = re.compile(r'<span>(\d*)人评价</span>')
    # 电影概况
    findInfoReg = re.compile(r'<span class="inq">(.*)</span>')
    data = []
    for i in range(10):
        url = baseUrl + str(i*25)
        html = askUrl(url)
        # print(html)
        # 处理数据
        soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('div',class_='item'):
            item = str(item)
            # 获取电影链接
            link = re.findall(findLinkReg,item)[0]
            # 存入data
            data.append(link)
            # 图片
            img = re.findall(findImgSrcReg,item)[0]
            data.append(img)
            # 标题
            title = re.findall(findTitleReg,item)[0]
            data.append(title)
            # 评分
            rating = re.findall(findRatingReg,item)[0]
            data.append(rating)
            #人数
            judge = re.findall(findJudgeReg,item)[0]
            data.append(judge)
            # 概况
            info = re.findall(findInfoReg,item)
            if len(info) != 0:
                info = info[0].replace('。','')
                data.append(info)
            else:
                data.append('')

    # for item in data:
    #     print(item)

    return data



# 请求url
def askUrl(baseUrl):
    # 设置请求头
    header = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.88Safari / 537.36'
    }
    # 请求
    request = urllib.request.Request(baseUrl,headers=header)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(e)

    # print(html)

    return html




if __name__ == '__main__':
    main()