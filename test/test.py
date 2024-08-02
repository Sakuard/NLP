# 假設 long_content 是您的長文本內容
long_content = "這邊是一個長文本內容的範例"

base_context_length = 4
shift_length = 2

# 進行迴圈切割
for start in range(0, len(long_content) - base_context_length + 1, shift_length):
    chunk = long_content[start:start + base_context_length]
    
    # 在這裡對 chunk 進行處理
    print(chunk)
    print("-" * 20)
