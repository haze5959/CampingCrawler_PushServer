from datetime import datetime
from datetime import timedelta

# 이틀 이상 차이날 경우 None 리턴
def get_reservation_open_between_now(reservation_code: str):
    info_list = reservation_code.split('/')
    open_interval = info_list[0]

    if open_interval == 'Y':
        # 예약 간격이 매년일 경우
        return None
    elif open_interval == 'M':
        # 예약 간격이 매월일 경우
        open_day_str = info_list[1]
        if len(open_day_str) > 0:
            open_day = int(open_day_str)
            now = datetime.now()
            if now.day == open_day:
                return 0
            else:
                after_one_date = now + timedelta(days=1)
                if after_one_date.day == open_day:
                    return 1
                else:
                    after_two_date = after_one_date + timedelta(days=1)
                    if after_two_date.day == open_day:
                        return 2
                    else:
                        return None
    elif open_interval == 'W':
        # 예약 간격이 매주일 경우
        open_week = info_list[1]
        week_num = weekday_to_num(open_week)

        now = datetime.now()
        if (week_num == now.weekday):
            return 0
        elif (week_num == now.weekday + 1):
            return 1
        elif (week_num == now.weekday + 2):
            return 2
        else:
            return None
    else:
        return None


def weekday_to_num(weekday: str):
    if (weekday == 'MON'):
        return 0
    elif (weekday == 'TUE'):
        return 1
    elif (weekday == 'WED'):
        return 2
    elif (weekday == 'THU'):
        return 3
    elif (weekday == 'FRI'):
        return 4
    elif (weekday == 'SAT'):
        return 5
    else:
        return 6
