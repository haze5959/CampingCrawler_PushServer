from datetime import datetime
from datetime import timedelta

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
        # var weekNum = DateTime.monday;
        # if (openWeek.isNotEmpty) {
        #   switch (openWeek) {
        #     case "MON":
        #       weekNum = DateTime.monday;
        #       break;
        #     case "TUE":
        #       weekNum = DateTime.tuesday;
        #       break;
        #     case "WED":
        #       weekNum = DateTime.wednesday;
        #       break;
        #     case "THU":
        #       weekNum = DateTime.thursday;
        #       break;
        #     case "FRI":
        #       weekNum = DateTime.friday;
        #       break;
        #     case "SAT":
        #       weekNum = DateTime.saturday;
        #       break;
        #     case "SUN":
        #       weekNum = DateTime.sunday;
        #       break;
        #     default:
        #       break;
        #   }

        #   final now = DateTime.now();
        #   var pivotDate = DateTime(now.year, now.month, now.day);
        #   pivotDate = pivotDate.add((Duration(days: weekNum - now.weekday)));
        #   if (now.isAfter(pivotDate)) {
        #     pivotDate = pivotDate.add(Duration(days: 7));
        #   }
        #   return [0, 1, 2, 3].map<DateTime>((index) {
        #     return pivotDate.add((Duration(days: 7 * index)));
        #   }).toList();
        # else:
        #   print("DateUtill param error!!!")
        #   return None
    else:
        return None
