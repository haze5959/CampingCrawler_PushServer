import os
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime
import redis
import fcmInfo
import urllib3
from pyfcm import FCMNotification
import mysql.connector

load_dotenv()
push_service = FCMNotification(api_key=fcmInfo["api_key"])

# mysql 설정
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_ID'),
    password=os.getenv('DB_PW'),
    database="camp"
)

# redis 설정
rd = redis.StrictRedis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=0,
    password=os.getenv('REDIS_PW')
)

# time_format = "%Y/%m/%d %H:%M"
# avail_dates_key = "availDates"

# 모든 캠핑장을 한번씩 돌아서 이전에 가지고 있는 값과 비교한다
# 새로생긴 "availDates"을 찾아내고 찾아낸 날짜 중 금토일월, 공휴일을 분리한다.

# * 캠핑장별
# 가까운 날짜순으로 한번만
# 조건중 위에서부터 아래 순서대로 우선순위

# - 주말 낀 연박 어떠세요?
# 조건: 금토일, 토일월

# - 주말에 캠핑 어떠세요?
# 조건: 토요일

# - 하루만 휴가내면 가능해요!
# 조건: 금 또는 일만 자리가 났을때

# 금토일 이외에는 알림없음!


# * 지역별
# 이번주것만 나타남
# 조건중 위에서부터 아래 순서대로 우선순위
def job_push_camp_avail_date():
    currentTime = datetime.now()
    if currentTime.hour >= 8:    # 8시 이후라면 실행한다
        print("")
        
# 전날 당일날 두번 알려준다.
def job_push_camp_reservation_date():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, name, area, reservation_open FROM site")
    myresult = mycursor.fetchall()
    for site in myresult:
        print(site)


if __name__ == "__main__":
    job_push_camp_avail_date()
    # 1시간에 한번씩 캠핑장 예약정보 체크
    schedule.every().hours.do(job_push_camp_avail_date)

    # 매일 9:30 에 예약일 알림
    schedule.every().day.at("9:30").do(job_push_camp_reservation_date)

    while True:
        schedule.run_pending()
        time.sleep(3600)  # 런루프
