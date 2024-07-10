from underthesea import ner, sent_tokenize
import numpy as np
import pickle
import nltk
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.cluster import KMeans

# Định nghĩa hàm tóm tắt văn bản
def text_summary(content):
    # Tiền xử lý và tách câu
    content_parsed = content.strip()
    sentences = sent_tokenize(content_parsed)

    num_sent = len(sentences) #số lượng của câu trong văn bản

    # Sử dụng NER để lấy từ được gắn nhãn
    word_labels = []
    for sentence in sentences:
        sentence_labels = ner(sentence)
        word_labels.extend([label[0] for label in sentence_labels])

    # Lọc các từ không phải là thực thể
    filtered_words = [word for word in word_labels if word not in ['B-PER', 'I-PER', 'B-LOC', 'I-LOC', 'B-ORG', 'I-ORG']]

    # Biểu diễn vector cho mỗi câu
    X = []
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        sentence_vec = np.zeros((len(filtered_words)))  # Sử dụng số chiều là độ dài danh sách các từ đã lọc
        for idx, word in enumerate(filtered_words):
            if word in words:
                sentence_vec[idx] = 1  # Đánh dấu 1 nếu từ có trong câu
        X.append(sentence_vec)

    # Tính số cụm cho K-means
    n_clusters = int(num_sent * (35/100))
    if n_clusters >= (num_sent - 1):
        return 'Văn bản quá ngắn! nhập văn bản dài hơn tôi sẽ tóm tắt giúp bạn'
    else:
        # Áp dụng K-means để training
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans = kmeans.fit(X)

        # Tính trung bình cho mỗi cụm
        avg = []
        for j in range(n_clusters):
            idx = np.where(kmeans.labels_ == j)[0]
            avg.append(np.mean(idx))

        # Tìm câu gần nhất với trung tâm của mỗi cụm
        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
        ordering = sorted(range(n_clusters), key=lambda k: avg[k])

        summary = ' '.join([sentences[closest[idx]] for idx in ordering]) #Đưa ra câu sau khi tóm tắt
        return summary
    

#hàm tìm kiếm yêu cầu tóm tắt trong câu đầu vào
def filter_texts(text):
    phrase = ["tóm tắt văn bản này sau đây:", "tom tat van ban sau đay:", "tom tat van ban sau đây", "tóm tắt văn bản sau đây",
                    "tóm tắt văn bản này: ", "tom tat van ban nay:", "tóm tắt văn bản này.", "tóm tăt van bản này", "tom tat van ban nay",
                    "rut gon van ban nay", "rút gọn văn bản này", "rut gon van ban nay:", "rút gọn văn bản này:",
                    "rút gon văn ban sau", "ru gọn văn bản sau", "tom tat van ban",
                    "tóm tắt văn ban","to tắt văn bản","tóm tắt văn bản", "tom tat van ban","tóm tắt văn bản:", "tom tat van ban:",
                    "tóm tắt:", "tom tat:", "tóm tắt:", "tom tát","tóm tat ","tom tắt", "tom tăt", "tóm tắt", "tom tat"]
    for start_phrase in phrase:
        # Chỉ xét 50 kí tự đầu tiên của đoạn văn
        first_fifty_chars = text[:50]
        if start_phrase in first_fifty_chars:
            start_index = first_fifty_chars.find(start_phrase)
            start_index += len(start_phrase)
            text = text[start_index:]
            number_text = len(text)

            if number_text > 50:
                return text.strip(), 1
    return text, 0

# a = "tóm tắt:  xin chào các bạn mình rất vui vid được gặp các bạn tại đây, làm cách nào để tìm ra bạn"

# b = filter_texts(a)[0]

# print(b)
