import streamlit as st
import sqlite3
import requests
import json
from datetime import datetime

# --- 1. การตั้งค่ามาตรฐาน (Identity & Style) ---
ST_ICON = "⭐" # KTK Icon according to memory
ST_TITLE = "Secretary V1 - James Protocol"

# --- 2. ส่วนของ "สมอง" (Database Layer) ---
def init_db():
    conn = sqlite3.connect('secretary_memory.db')
    c = conn.cursor()
    # สร้างตารางถ้ายังไม่มี (Mandatory Checklist: Persistent Storage)
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (timestamp TEXT, category TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_memory(category, content):
    conn = sqlite3.connect('secretary_memory.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?, ?, ?)", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category, content))
    conn.commit()
    conn.close()

# --- 3. ส่วนของ "ปาก" (Communication Protocol) ---
def send_line_standard(msg):
    # แก่นของโปรโตคอล: คุยตรงกับ LINE ไม่ผ่าน Library ซับซ้อน
    url = 'https://api.line.me/v2/bot/message/broadcast'
    token = 'ใส่_TOKEN_ของพี่ตรงนี้' # พี่นำ Token มาใส่จุดนี้
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        "messages": [{"type": "text", "text": f"{ST_ICON} [James Secretary]:\n{msg}"}]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.status_code
    except:
        return 500

# --- 4. ส่วนหน้าจอ (User Interface Layer) ---
def main():
    st.set_page_config(page_title=ST_TITLE, page_icon=ST_ICON)
    st.title(f"{ST_ICON} {ST_TITLE}")
    
    init_db()

    # ช่องรับข้อมูล (The Interface)
    category = st.selectbox("หมวดหมู่การจดบันทึก", ["General", "Trading Logic", "Personal Audit"])
    user_input = st.text_area("สั่งงานเลขาหรือบันทึกข้อมูลที่นี่...", placeholder="พิมพ์สิ่งที่พี่ต้องการให้เลขาจำ...")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("บันทึกลงสมอง (Save)"):
            if user_input:
                save_memory(category, user_input)
                st.success("เลขาบันทึกเรียบร้อยแล้วครับพี่")
            else:
                st.warning("พี่ต้องพิมพ์ข้อมูลก่อนนะครับ")

    with col2:
        if st.button("แจ้งเตือนเข้า Line (Push)"):
            if user_input:
                status = send_line_standard(user_input)
                if status == 200:
                    st.info("ส่งข้อมูลเข้า Line เรียบร้อยครับ")
                else:
                    st.error(f"การเชื่อมต่อติดขัด (Code: {status})")

    # ส่วนแสดงผลความจำ (Memory Audit)
    st.divider()
    st.subheader("📋 รายการบันทึกล่าสุด")
    conn = sqlite3.connect('secretary_memory.db')
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 5", conn)
    st.table(df)
    conn.close()

if __name__ == "__main__":
    main()
