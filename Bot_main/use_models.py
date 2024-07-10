import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import numpy as np
import random
from .acronym.dictions_city import normalize_text_city, find_city, normalize_city
from .Name_person import find_name
from .Text_summary import text_summary, filter_texts
from .City_weather import wt_main


class BotPredictor:
    def __init__(self, data_file='Bot_main/Data/mains.json', model_file='Bot_main/Models/mains.h5'):
        self.data_file = data_file
        self.model_file = model_file
        self.tokenizer, self.unique_labels, self.intents = self.prepare_mains()
        self.model = load_model(self.model_file)

    def prepare_mains(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)

        intents = data['intents']
        sentences = []
        labels = []
        label_dict = {}

        for intent in intents:
            for pattern in intent['patterns']:
                sentences.append(pattern)
                labels.append(intent['tag'])
                if intent['tag'] not in label_dict:
                    label_dict[intent['tag']] = len(label_dict)

        labels = [label_dict[label] for label in labels]
        unique_labels = list(label_dict.keys())
        tokenizer = Tokenizer(oov_token="<OOV>")
        tokenizer.fit_on_texts(sentences)

        return tokenizer, unique_labels, intents

    def predict(self, input_sentence):
        input_sequence = self.tokenizer.texts_to_sequences([input_sentence])
        input_sequence = pad_sequences(input_sequence, padding='post')
        if input_sequence.shape[1] > 0:
            predictions = self.model.predict(input_sequence)
            predicted_class = np.argmax(predictions)
            confidence = np.max(predictions)
            response_tag = self.unique_labels[predicted_class]
            return response_tag, confidence, predicted_class
        else:
            # Handle the case when input_sequence is empty
            # You can modify this part based on your needs
            return None, None, None

    def get_response(self, response_tag):
        for intent in self.intents:
            if intent['tag'] == response_tag:
                return random.choice(intent['responses']), random.choice(intent['responses_1'])
        return ""
    
    def khong_hieu(self, input_sentence):
        response_tag, confidence, predicted_class = self.predict(input_sentence)
        class_khong_hieu = self.unique_labels[-1]
        response = self.get_response(class_khong_hieu)
        return response[0], confidence, predicted_class
        
    def mains(self, input_sentence, classes):
        response_tag, confidence, predicted_class = self.predict(input_sentence)
        if predicted_class not in classes:
            return self.khong_hieu(input_sentence)
        else:
             response = self.get_response(response_tag)
             return response[0], confidence, predicted_class

    def ten(self, input_sentence, classes):
        name = find_name(input_sentence)

        response_tag, confidence, predicted_class = self.predict(input_sentence)
        if name != '0':
            if predicted_class not in classes:
                return self.khong_hieu(input_sentence)
            else:
                response = self.get_response(response_tag)
                return response[0] + name.title() + response[1], confidence, predicted_class
        else: 
            return "Tôi không biết tên bạn là gì, bạn có thể cung cấp lại tên của bạn không", confidence, predicted_class
        
    def tom_tat(self, input_sentence, classes):
        response_tag, confidence, predicted_class = self.predict(input_sentence)
        if confidence < 0.7:
            a = text_summary(input_sentence)
            return a, confidence, predicted_class
        
        else: 
            response = self.get_response(response_tag)
            return response[0], confidence, predicted_class
        
    def weather_all(self, input_sentence, classes):
        response_tag, confidence, predicted_class = self.predict(input_sentence)
        if predicted_class not in classes:
            return self.khong_hieu(input_sentence)
        else:
            response = self.get_response(response_tag)
            weather = wt_main(input_sentence)
            return weather, confidence, predicted_class
        
    def nhiet_do(self, input_sentence, classes):
        response_tag, confidence, predicted_class = self.predict(input_sentence)
        if predicted_class not in classes:
            return self.khong_hieu(input_sentence)
        else:
            response = self.get_response(response_tag)
            weather = str(wt_main(input_sentence))
            return weather, confidence, predicted_class

    def print_label_mapping(self):
        print("Mapping giữa lớp và nhãn:")
        for index, label in enumerate(self.unique_labels):
            print(f"Lớp {index}: Nhãn '{label}'")



x = BotPredictor()
p = x.print_label_mapping()
print(p)

name_city = '0'
cla = 0
waiting_summary = 0
origin_classes = [0,3,4,5,9,11,12,13,14,16,21,23,25,27,31,32,33,34]
classes = [0,3,4,5,9,11,12,13,14,16,21,23,25,27,31,32,33,34]
def get_responses(input_sentence):
    global waiting_summary
    global classes
    global cla
    global name_city
    text_stand = normalize_text_city(input_sentence)
    # print("người dùng nhập vào là: ",text_stand)
    input_text = normalize_city(text_stand)

    a, b, c = x.mains(input_text, classes)

    if filter_texts(input_sentence)[1] == 1:
        a = text_summary(input_sentence)

    elif waiting_summary == 1:
        a,b,c = x.tom_tat(input_text, classes)
        waiting_summary = 0
        # if b > 0.95:
        #     a,b,c = x.mains(input_text, classes)

    elif c == 0:
        classes = origin_classes + [1,2]

    elif c == 4: 
        classes = origin_classes
        a,b,c = x.ten(input_text, classes)

    elif c == 5: 
        classes = origin_classes + [6,7,8]
            
    elif c == 9:
        classes = origin_classes +[10]

    elif c == 16:
        if name_city == "":
            a,b,c = x.weather_all(text_stand, classes)
            a = f'Tại {a[0]}, hiện tại {a[1]}, nhiệt độ đo được {a[2]}℃ - nhiệt độ cảm nhận là {a[3]}℃ có độ ẩm {a[5]}% và áp suất khí quyển là {a[4]} hPa'
        cla = 16
        classes = origin_classes + [17,18,19]
   
    #Xử lý sau khi câu chat thời tiết đầu tiên không cung cấp tên thành phố
    elif c == 18:
            name_city = find_city(text_stand)
            classes = origin_classes + [17,19]
            if cla == 16:
                a,b,c = x.weather_all(text_stand, classes)
                a = f'Tại {a[0]}, hiện tại {a[1]}, nhiệt độ đo được {a[2]}℃ - nhiệt độ cảm nhận là {a[3]}℃ có độ ẩm {a[5]}% và áp suất khí quyển là {a[4]} hPa'
                cla = 18

            elif cla == 21:
                a,b,c = x.weather_all(text_stand, classes)
                a = f'Nhiệt độ hiện tại ở {name_city} là {a[2]}℃'
                cla = 18

            elif cla == 18:
                a,b,c = x.weather_all(text_stand, classes)
                a = f'Tại {a[0]}, hiện tại {a[1]}, nhiệt độ đo được {a[2]}℃ - nhiệt độ cảm nhận là {a[3]}℃ có độ ẩm {a[5]}% và áp suất khí quyển là {a[4]} hPa'
                cla = 18
            # a = wt_main(text_stand)

    elif c== 20:
        classes = origin_classes
        name_city = find_city(text_stand)
        if find_city(text_stand) != "0":
            a,b,c = x.weather_all(text_stand, classes)
            a = f'Tại {a[0]}, hiện tại {a[1]}, nhiệt độ đo được {a[2]}℃ - nhiệt độ cảm nhận là {a[3]}℃ có độ ẩm {a[5]}% và áp suất khí quyển là {a[4]} hPa'
            # a = ' '.join(map(str, a[:5]))

    elif c == 21:
        classes = origin_classes + [22]
        # name_city = find_city(text_stand)
        if cla == 18:
            a,b,c = x.weather_all(name_city, classes)
            a = f'nhiệt độ hiện tại ở {name_city} là {a[2]}℃'
            cla = 21
        cla = 21

        # else:
        #     if find_city(text_stand) != "0":
        #         a,b,c = x.weather_all(text_stand, classes)
        #         a = a[2]
        
    elif c == 23:
        classes = origin_classes + [24]

    elif c == 25:
        classes = origin_classes + [26]

    elif c == 27:
        classes = origin_classes + [28,29,30]
        # a,b,c = x.mains(input_text, classes)
        waiting_summary = 1

    # return a, '\nlớp: ',c, '\nđộ tin cậy:', b
    return a

# while True:
#     a = input('Nhập: ')
#     if a == "q":
#         break
#     print(get_responses(a))


