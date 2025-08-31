import requests
import random
import schedule
import time
import threading
from flask import Flask
from openai import OpenAI
import os

# ==== CONFIG từ Environment Variables ====
API_TOKEN = os.getenv("API_TOKEN")   # Telegram Bot Token
CHAT_ID = os.getenv("CHAT_ID")       # Chat ID của bạn
OPENAI_KEY = os.getenv("OPENAI_KEY") # OpenAI API Key

client = OpenAI(api_key=OPENAI_KEY)
app = Flask(__name__)

def send_message(text):
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def generate_vocab():
    prompt = """
    Hãy đưa ra 10 từ vựng tiếng Nhật ngẫu nhiên theo chủ đề (level N5–N1 bất kỳ),
    kèm:
    - Kanji
    - Hiragana/Katakana
    - Nghĩa tiếng Việt
    - Âm Hán Việt
    - Cách đọc âm On, âm Kun
    - Ví dụ câu
    - Giải thích ngữ pháp trong câu
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def daily_vocab():
    vocab = generate_vocab()
    send_message("📚 今日の日本語単語 (Từ vựng hôm nay):\n\n" + vocab)

daily_vocab()

# def run_schedule():
#     schedule.every().day.at("07:30").do(daily_vocab)
#     while True:
#         schedule.run_pending()
#         time.sleep(60)

@app.route('/')
def index():
    return "Japanese Telegram Bot is running!"

if __name__ == "__main__":
    t = threading.Thread(target=run_schedule)
    t.start()
    app.run(host="0.0.0.0", port=10000)
