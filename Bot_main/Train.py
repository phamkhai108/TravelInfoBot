# Import các thư viện cần thiết
import tensorflow as tf
from tensorflow.keras import layers
import json
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


# Đọc dữ liệu từ file JSON
with open('Data/mains.json', 'r') as f:
    data = json.load(f)

# Chuẩn bị dữ liệu
intents = data['intents']

# Tạo danh sách các câu và nhãn tương ứng
# Tạo danh sách các câu và nhãn tương ứng
sentences = []
labels = []
label_dict = {}
for intent in intents:
    for pattern in intent['patterns']:
        sentences.append(pattern)
        labels.append(intent['tag'])
        if intent['tag'] not in label_dict:
            label_dict[intent['tag']] = len(label_dict)

# Chuyển đổi nhãn sang dạng số
labels = [label_dict[label] for label in labels]
unique_labels = list(label_dict.keys())

# In ra tên các lớp tương ứng với danh sách nhãn
for i, label in enumerate(unique_labels):
    print(f"Nhãn {i}: {label}")


# Tokenize và pad sequences
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(sentences)
sequences = tokenizer.texts_to_sequences(sentences)
padded_sequences = pad_sequences(sequences, padding='post')

# Chia dữ liệu thành tập huấn luyện và tập kiểm thử
# train_sequences, test_sequences, train_labels, test_labels = train_test_split(padded_sequences, labels, test_size=0.25)
train_sequences = padded_sequences
train_labels = labels

max_features = len(tokenizer.word_index) + 1
embedding_dim = 128
number_label = len(unique_labels)

max_sequence_length = max([len(seq) for seq in train_sequences])



# Chuyển đổi dữ liệu huấn luyện thành tập dữ liệu TensorFlow
# train_dataset = tf.data.Dataset.from_tensor_slices((train_sequences, train_labels))

# # Trộn dữ liệu
# train_dataset = train_dataset.shuffle(buffer_size=1024)

# # Thêm batch size
# train_dataset = train_dataset.batch(3)

model = tf.keras.Sequential([
    layers.Embedding(max_features, embedding_dim),
    layers.LSTM(72, activation='relu', return_sequences=True),
    layers.Dense(72, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    # layers.Dense(64, activation='relu'),
    layers.GlobalAveragePooling1D(),
    layers.BatchNormalization(),
    layers.Dropout(0.1),
    layers.Dense(number_label, activation='softmax')
])

early_stop = EarlyStopping(monitor='val_loss', patience=10)
callbacks_list = [early_stop]
model.summary()
optimizer = Adam(learning_rate=0.0001)
model.compile(loss='sparse_categorical_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])

# Huấn luyện mô hình
history = model.fit(train_sequences, np.array(train_labels),
                    # validation_data=(test_sequences, np.array(test_labels)),
                    epochs=70,
                    batch_size = 2
                    # callbacks=callbacks_list
                    )

model.save('Models/mains.h5')