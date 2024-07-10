import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import regularizers
from Bot_main.Prepare_data import prepare_data, file_names_list

# Chuẩn bị dữ liệu
words, labels, training, output = prepare_data(file_names_list)

def create_model():
    model = Sequential()

    # Lớp thứ ba với 32 đơn vị và hàm kích hoạt 'relu'
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))

    # Lớp cuối cùng với số đơn vị bằng độ dài của output[0] và hàm kích hoạt softmax
    model.add(Dense(len(output[0]), activation='softmax'))

    # Biên dịch mô hình với hàm mất mát là categorical_crossentropy, optimizer là adam và metrics là accuracy
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    try:
        # Nếu file model.h5 tồn tại, tải trọng số từ file
        model.load_weights("Bot_main/Models/mains.h5")
    except:
        # Nếu file model.h5 không tồn tại, huấn luyện mô hình với dữ liệu training và output
        model.fit(training, output, epochs=50, batch_size=8)
        # Lưu trọng số của mô hình vào file model.h5
        model.save("Bot_main/Models/mains.h5")
    
    return model

# Sử dụng hàm create_model để tạo mô hình
model = create_model()
# model.build((None, len(training[0])))
model.summary()
