import re
from unidecode import unidecode

def extract_name(sentence):
    # Tạo một list các biểu thức chính quy để tìm kiếm các mẫu khác nhau
    patterns = [
        r'toi ten la ([\w\s]+)',
        r'ten cua toi la ([\w\s]+)',
        r'ten cua toi do la ([\w\s]+)',
        r'ten toi la ([\w\s]+)',
        r'ten toi do la ([\w\s]+)',
        r'ten toi ([\w\s]+)',
        r'tôi tên là ([\w\s]+)',            # Có dấu
        r'tôi tên là ([\w\s]+)',            # Có dấu
        r'tên của tôi (?:dường như là|hình như|dường như|là) ([\w\s]+)',        # Có dấu
        r'tên của tôi do là ([\w\s]+)',     # Có dấu
        r'tên tôi là ([\w\s]+)',            # Có dấu
        r'tên tôi do là ([\w\s]+)',         # Có dấu
        r'tôi tên ([\w\s]+)', 
        r'tôi ten ([\w\s]+)', 
        r'toi tên ([\w\s]+)', 
        r'toi ten ([\w\s]+)', 
        r'tôi là ([\w\s]+)', 
        r'tôi la ([\w\s]+)', 
        r'toi là ([\w\s]+)', 
        r'toi la ([\w\s]+)', 

        r'([^\s,]+)\s+đó là tên của tôi',
        r'([^\s,]+)\s+do là tên của tôi',
        r'([^\s,]+)\s+do la ten cua toi',
        r'([^\s,]+)\s+là tên của mình',  
        r'([^\s,]+)\s+la ten cua minh',
        r'([^\s,]+)\s+la ten cua toi',
        r'([^\s,]+)\s+la ten toi',
        r'([^\s,]+)\s+do la ten toi',
        r'([^\s,]+)\s+la ten minh',
        r'([^\s,]+)\s+la ten to',
        r'([^\s,]+)\s+la ten cua to',
        r'([^\s,]+)\s+là tên của tôi',
        r'([^\s,]+)\s+là tên của tôi',   
        r'([^\s,]+)\s+là tên của mình',  
        r'([^\s,]+)\s+là tên tôi',       
        r'([^\s,]+)\s+là tên của tôi',   
    ]
    
    # Lặp qua các mẫu và tìm kiếm
    for pattern in patterns:
        match = re.search(pattern, sentence, re.IGNORECASE)  # Sử dụng cờ re.IGNORECASE
        if match:
            if len(match.groups()) > 0:
                return match.group(1)  # Trả về phần giá trị sau mẫu nếu có
            else:
                return match.group(0)  # Trả về phần trước mẫu nếu có
            
    return None  # Trả về None nếu không tìm thấy

#hàm tách văn bản thành các câu để dự đoán tên chính xác
def find_name(text):
    sentences = re.split(r'[.,?/\'"!]', text)  # Tách văn bản thành các câu bởi dấu . hoặc ,
    name = '0'
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            extracted_name = extract_name(sentence)
            if extracted_name:
                name = extracted_name
    return name

# while True:
#     a = input('Nhập tên: ')
#     print(find_name(a))