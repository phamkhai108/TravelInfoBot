import requests
import datetime
from .acronym.dictions_city import normalize_text_city, normalize_city, find_city, normalized_words


def wt_main(name_city):
    #gọi hàm để lọc tên city từ câu và chuyển xuống chữ thường
    name_city = find_city(name_city)
    name_city_lower = name_city.lower()

    api_key = '81d9e02d5e6f4c2c775148ffa556977d' 
    url = f'http://api.openweathermap.org/data/2.5/weather?q={name_city_lower}&appid={api_key}&lang=vi&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        #mô tả thời tiết
        weather_description = data['weather'][0]['description']
        #nhiệt độ hiện tại
        temperature = data['main']['temp']  # Chuyển đổi nhiệt độ từ Kelvin sang Celsius
        #nhiêt độ nhận thức
        feels_like = data['main']['feels_like']
        #áp suất khí quyẻn trên mực nước biển
        pressure = data['main']['pressure']
        #Độ ẩm %
        humidity = data['main']['humidity']
        #áp suất khí quyển trê mặt đắt
        # grnd_level = data['main']['grnd_level']
        #tốc độ gió
        wind_speed = data['wind']['speed']
        # Hướng gió
        wind_deg = data['wind']['deg']
        if (wind_deg<23 or wind_deg>336):
            wind_deg = 'Bắc'

        elif (wind_deg>=23):
            wind_deg = 'Đông Bắc'

        elif (wind_deg>67):
            wind_deg = 'Đông'

        elif (wind_deg>=113):
            wind_deg = 'Đông Nam'

        elif (wind_deg>158):
            wind_deg = 'Nam'

        elif (wind_deg>=202):
            wind_deg = 'Tây Nam'

        elif (wind_deg>248):
            wind_deg = 'Tây'

        elif (wind_deg>=293):
            wind_deg = 'Tây Bắc'
        else: 
            wind_deg = 'Tây Bắc'
        # Mức độ mây
        clouds_all = data['clouds']['all']
        # Giờ hiện tại
        current_time = datetime.datetime.fromtimestamp(data['dt']).strftime('%H Giờ: %M Phút, Ngày %d-%m-%Y')
        # Thời gian mặt trời lên
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H Giờ: %M Phút, Ngày %d-%m-%Y')
        # Thời gian mặt trời xuống
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H Giờ: %M Phút, Ngày %d-%m-%Y')
        # Tên quốc gia
        country = data['sys']['country']

        '''
        Danh sách như sau: 
        0: Tên thành phố, 1: mô tả thời tiết, 2: nhiệt độ hiện tại, 3: nhiệt độ cảm nhận,
        4: Áp suất khí quyển trên mặt nước biển Pa, 5: độ ẩm %, áp suất khi quyển trên mặt đất Pa, 6: tốc độ gió Km/h, 
        7: hướng gió, mức độ mây, giờ hiện tại, 8: thời gian mặt trời lên, 9: thời gian mặt trời xuống,
        10: tên quốc gia.
        '''
        
        return (name_city, weather_description, temperature, feels_like, pressure,
                 humidity, wind_speed, wind_deg, clouds_all, current_time, 
                sunrise, sunset, country)

    else: 
        return ('''Xin lỗi API truy cập thông tin thời tiết của chúng tôi bị lỗi
                 nên không lấy được thông tin thời tiết hiện tại.
                 Bạn có thể đặt câu hỏi khác tôi sẽ giúp bạn.''', '','','','','','','','','','','')



# sentence = 'tHời tiết tại Ha NOi'
# print(wt_main(sentence))




