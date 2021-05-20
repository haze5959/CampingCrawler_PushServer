import schedule 
import time 
import datetime
import redis
from Script import gimpo_munsoogol
from Script import inchoen_tree
from redisAccount import accountInfo
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

time_format = "%Y/%m/%d %H:%M"
avail_dates_key = "availDates"
updated_time_key = "updateTime"

camp_munsoo_key = "camp_munsoo"
camp_tree_key = "camp_tree"

def job_crawlingCampingSite(): 
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
    job_crawlingCampingSite()
    ## 1시간에 한번씩 실행 
    schedule.every().hours.do(job_crawlingCampingSite) 

    while True: 
        schedule.run_pending() 
        time.sleep(3600) # 런루프