import schedule 
import time 
import datetime
import redis
import accountInfo
import fcmInfo
import urllib3
from pyfcm import FCMNotification

push_service = FCMNotification(api_key=fcmInfo["api_key"])

# time_format = "%Y/%m/%d %H:%M"
# avail_dates_key = "availDates"

# 모든 캠핑장을 한번씩 돌아서 이전에 가지고 있는 값과 비교한다
# 새로생긴 "availDates"을 찾아내고 찾아낸 날짜 중 금토일월, 공휴일을 분리한다.
#  

# * 캠핑장별
# 가까운 날짜순으로 한번만
# 조건중 위에서부터 아래 순서대로 우선순위

# - 주말 낀 연박 어떠세요?
# 조건: 금토일, 토일월

# - 주말에 캠핑 어떠세요?
# 조건: 토요일

# - 하루만 휴가내면 가능해요!
# 조건: 금 또는 일만 자리가 났을때


# * 지역별
# 이번주것만 나타남
# 조건중 위에서부터 아래 순서대로 우선순위

def job_push_camp_avail_date(): 
    currentTime = datetime.datetime.now()
    if currentTime.hour >= 8:    # 8시 이후라면 실행한다
        # redis 설정
        host = accountInfo['host']
        port = accountInfo['port']
        password = accountInfo['pw']
        rd = redis.StrictRedis(host=host, port=port, db=0, password=password)
        
        # 문수골 캠핑장 크롤링
        camp_munsoo_availDate = gimpo_munsoogol.availableDate()
        print("[{camp}] Avail date: {dates}".format(camp=camp_munsoo_key, dates=camp_munsoo_availDate))
        rd.hset(camp_munsoo_key, avail_dates_key, ','.join(camp_munsoo_availDate))

        currentTime = datetime.datetime.now()
        print("[{camp}] Crawling Time: {time}".format(camp=camp_munsoo_key, time=currentTime))
        rd.hset(camp_munsoo_key, updated_time_key, currentTime.strftime(time_format))
    
if __name__ == "__main__":
    job_push_camp_avail_date()
    ## 1시간에 한번씩 실행 
    schedule.every().hours.do(job_push_camp_avail_date) 

    while True: 
        schedule.run_pending() 
        time.sleep(3600) # 런루프