import datetime
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def getHTMLText(url):
    try:
        cook = {"Cookie": 'BAIDUID=FE0F97F1FC37C47792091A2523CD945F:FG=1; HMACCOUNT=CC6D0E280C842123'}
        header = {'Referer': 'https://www.baidu.com/','user-agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
        header= {"Accept": "*/*","Accept-Encoding": "gzip, deflate","Host": "httpbin.org",'Referer': 'https://www.baidu.com/','user-agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
        head = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "httpbin.org",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}


        r = requests.get(url, headers = header, cookies=cook ,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("请求异常")

def sendEmail(receivers, from_web, origin, time, title, artical, name):
    # 文章题目和正文内容
    Subject = '【' + from_web + '】' + title + '(' + time + ')' + '[' + name + ']'
    basisinfo = '<h1>' + title + '</h1>'
    basisinfo2 = '<h3>' + '发布时间：' + time + '</h3>'
    basisinfo3 = '<h3>' + '所属栏目：' + '[' + from_web + '] [' + name + ']' + '</h3>'
    CONTENT = origin + basisinfo2 + basisinfo3 + basisinfo + str(artical)
    # 第三方 SMTP 服务
    mail_host = "XXXXXXXXXXXXXXXX"      # 你的邮箱服务器
    mail_user = "XXXXXXXXXXXXXXXX"      # 你的邮箱账号
    mail_pass = "XXXXXXXXXXXXXXXX"      # 你的邮箱密码（授权码）
    mail_port = 25
    # 邮件内容构造
    msg = MIMEText( CONTENT ,"html" ,"utf-8")
    msg['Subject'] = Subject
    msg['From'] = mail_user
    msg['To']=",".join(receivers)
    #发送邮件
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_port)
        res = smtpObj.login(mail_user, mail_pass)
        print("登录结果：",res)
        smtpObj.sendmail(from_addr=mail_user, to_addrs=receivers, msg=msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

if __name__ == "__main__":
    # 收件人
    receivers = ['XXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXX']        # 收件人列表
    # 当天日期
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    # 爬取当日教务处信息
    from_web = '教务处'
    urls1 = ['http://jwc.ahu.edu.cn/jwkx/list.htm','http://jwc.ahu.edu.cn/10314/list.htm']
    names1 = ['教务快讯','通知公告']
    for index, url in enumerate(urls1):
        print("正在搜索教务处通知信息" + str(index) + "...")
        soup = BeautifulSoup(getHTMLText(url), "html.parser")
        tags = soup.find_all("li", attrs={'class': "bg1"})
        for tag in tags:
            # tag信息预处理
            link = 'http://jwc.ahu.edu.cn' + tag.a.attrs['href']  # 链接
            origin = '<a href=' + link + '>原文链接</a>'  # 原始链接
            time = tag.span.text                # 发布时间
            soup_info = BeautifulSoup(getHTMLText(link), "html.parser")     # 具体网页内容
            title = soup_info.find('td', attrs={'bgcolor': "#f7f7f7"}).text     # 文章标题
            artical = soup_info.find('div', attrs={'class': "wp_articlecontent"})    # 文章内容
            if time == today:
                sendEmail(receivers, from_web, origin, time, title, artical, names1[index])
    # 爬取当日互院信息
    from_web = '互院'
    urls2 = ['http://si.ahu.edu.cn/15490/list.htm','http://si.ahu.edu.cn/xwgg_9326/list.htm','http://si.ahu.edu.cn/tzgg/list.htm']
    names2 = ['党建园地', '新闻动态', '通知公告']
    for index, url in enumerate(urls2):
        print("正在搜索互联网学院通知信息" + str(index) + "...")
        soup = BeautifulSoup(getHTMLText(url), "html.parser")
        aaa = soup.find_all("ul", attrs={'class': 'news_list list2' })
        soup = BeautifulSoup(str(aaa), "html.parser")
        tags = soup.find_all('li')
        for tag in tags:
            # tag信息预处理
            link = 'http://si.ahu.edu.cn/' + tag.a.attrs['href']  # 链接
            origin = '<a href=' + link + '>原文链接</a>'  # 原始链接
            time = tag.find('span', attrs={'class': "news_meta"}).text  # 发布时间
            soup_info = BeautifulSoup(getHTMLText(link), "html.parser")  # 具体网页内容
            title = soup_info.find('h1', attrs={'class': "arti_title"}).text  # 文章标题
            artical = soup_info.find('div', attrs={'class': "wp_articlecontent"})  # 文章内容
            # if time == today:
            #     sendEmail(receivers, from_web, origin, time, title, artical)
            sendEmail(receivers, from_web, origin, time, title, artical, names2[index])
            break
