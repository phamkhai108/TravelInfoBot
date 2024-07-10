import datetime
from datetime import timedelta

def times():
    now = datetime.datetime.now()
    seven_hours_later = now + timedelta(hours=7)
    
    time_day = seven_hours_later.strftime('%d')
    time_month = seven_hours_later.strftime('%m')
    time_year = seven_hours_later.strftime('%y')
    time_hour = seven_hours_later.strftime('%H')
    time_minutes = seven_hours_later.strftime('%M')
    time_second = seven_hours_later.strftime('%S')

    return 'ngày ' + time_day, 'tháng ' + time_month, 'năm 20' + time_year, time_hour + ' giờ', time_minutes + ' phút', time_second + ' giây'

def times_1(day, hour, minutes):
    now = datetime.datetime.now()
    # Chỉ sử dụng days, hours và minutes vì timedelta không hỗ trợ years và months
    seven_hours_later = now + datetime.timedelta(days=day, hours=hour+7, minutes=minutes)
    
    time_day = seven_hours_later.strftime('%d')
    time_month = seven_hours_later.strftime('%m')
    time_year = seven_hours_later.strftime('%y')
    time_hour = seven_hours_later.strftime('%H')
    time_minutes = seven_hours_later.strftime('%M')
    time_second = seven_hours_later.strftime('%S')
    
    return 'ngày ' + time_day, 'tháng ' + time_month, 'năm 20' + time_year, 'giờ ' + time_hour, 'phút ' + time_minutes, 'giây ' + time_second

# print(times_1(0, 848, 0))
