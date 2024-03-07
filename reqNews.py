import requests
import json
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from myConfig import *

def fetch_data_and_send_email():
    url = "https://oas.gdut.edu.cn/seeyon/ajax.do?method=ajaxAction&managerName=newsDataManager&rnd=66369"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": "JSESSIONID=c45848c7-7148-4b61-abd7-499f07e7f65e; avatarImageUrl=-6964000252392685202; safedog-flow-item=2D0FF26BB5D1F1F77FB3CCF6EA9DCFEE; route=ae2d147b4fc226d85e8d79c507516d58; wzws_sessionid=gWQ5NGEyN6Bl6AgHgjRhMmZkNIAxODMuNjMuMTE5LjU2; loginPageURL=",
        "Origin": "https://oas.gdut.edu.cn",
        "Referer": "https://oas.gdut.edu.cn/seeyon/newsData.do?method=newsIndex&spaceType=2&fragmentId=5854888065150372255&ordinal=0&panelValue=designated_value",
        "RequestType": "AJAX",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122")',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    payload = {
        "managerMethod": "findListDatas",
        "arguments": '[{"pageSize":"20","pageNo":1,"listType":"1","spaceType":"2","spaceId":"","typeId":"","condition":"publishDepartment","textfield1":"","textfield2":"","myNews":"","fragmentId":"5854888065150372255","ordinal":"0","panelValue":"designated_value"}]'
    }
    session = requests.Session()
    session.trust_env = False
    response = session.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = json.loads(response.text)
        news_list = list(data['list'])
        all_text = ""
        for idx, item in enumerate(news_list):
            path = 'https://oas.gdut.edu.cn/seeyon/newsData.do?method=newsView&newsId={}&from=&spaceId='
            path = path.format(item['id'])
            all_text += f"<h3>{idx+1}.{item['title']}\n</h3><hr/>{item['content']}{item['publishUserDepart']}\n{item['publishDate1']}\n[{item['typeName']}]\n<a href='{path}'>{path}</a>\n\n"
            # print()
        send_email(all_text)
    else:
        print("Failed to fetch data")


def send_email(data):
    # 设置发件人邮箱信息
    # print(from_email)
    # print(from_pwd)
    # print(port)
    # print(server_address)
    # print(to_email)
    sender_email = from_email
    sender_password = from_pwd

    # 设置收件人邮箱信息
    receiver_email = to_email
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"GDUT-News{now_time}"

    # 添加邮件内容
    body = MIMEText(str(data), 'plain')
    msg.attach(body)

    # 发送邮件
    with smtplib.SMTP(server_address, port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    print(f'发送成功!{now_time}')


def plan_time():
    print("任务已启动，每天12:00和0:00推送消息")
    schedule.every().day.at("12:00").do(fetch_data_and_send_email)
    schedule.every().day.at("00:00").do(fetch_data_and_send_email)

    # 持续运行程序，直到任务完成
    while True:
        schedule.run_pending()
        time.sleep(60 * 30)  # 等待一分钟


if __name__ == '__main__':
    plan_time()
    # fetch_data_and_send_email()