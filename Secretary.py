import streamlit as st
import sqlite3
from datetime import datetime

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="Secretary V1", page_icon="⭐", layout="wide")

# ปรับแต่ง CSS เล็กน้อยเพื่อให้ตารางดูประณีตขึ้น
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. DATABASE ENGINE ---
def get_db_connection():
    return sqlite3.connect('secretary_memory.db', check_same_thread=False)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS legacy_log 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp TEXT, 
                  category TEXT, 
                  content TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- 3. UI LOGIC ---
st.title("⭐ Secretary V1: The Identity Keeper")
st.caption("ระบบรวบรวมตะกอนความคิด - User: Kriangkrai (James)")

# Sidebar 
with st.sidebar:
    st.header("⚙️ เมนูควบคุม")
    mode = st.radio("เลือกโหมดการทำงาน", ["📥 บันทึกข้อมูล", "📖 เรียกดูคลังความจำ"])
    st.markdown("---")
    st.write("สถานะระบบ: **Online**")

if mode == "📥 บันทึกข้อมูล":
    st.subheader("บันทึกสิ่งที่ตกตะกอนลงในจิตใต้สำนึกดิจิทัล")
    with st.form("identity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("หมวดหมู่", 
                                  ["การเทรด (Logic/Strategy)", 
                                   "จิตวิทยา (Mindset/Soul)", 
                                   "ครอบครัว (Legacy/Education)", 
                                   "เทคโนโลยี (Code/AI)"])
        with col2:
            status = st.select_slider("ความสำคัญ", options=["ทั่วไป", "สำคัญ", "กฎเหล็ก"])
        
        content = st.text_area("รายละเอียดประสบการณ์/สิ่งที่เรียนรู้:", height=200)
        
        submit = st.form_submit_button("บันทึกข้อมูลถาวร")
        
        if submit and content:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO legacy_log (timestamp, category, content, status) VALUES (?, ?, ?, ?)",
                      (now, category, content, status))
            conn.commit()
            conn.close()
            st.success("✅ บันทึกสำเร็จ: ข้อมูลถูกจัดเก็บเรียบร้อยครับพี่เกรียง")

else:
    st.subheader("คลังความจำที่ตกตะกอนแล้ว (History)")
    conn = get_db_connection()
    c = conn.cursor()
    # ดึงข้อมูลโดยตรงจาก SQLite
    c.execute("SELECT timestamp, category, content, status FROM legacy_log ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    
    if data:
        # กำหนดหัวตาราง
        header = ["วัน-เวลา", "หมวดหมู่", "เนื้อหาที่บันทึก", "ระดับความสำคัญ"]
        
        # แสดงผลในรูปแบบ Table ของ Streamlit (Lightweight)
        # เราแปลงข้อมูลเป็น list ของ dict เพื่อความอ่านง่าย
        display_data = []
        for row in data:
            display_data.append({
                "วัน-เวลา": row[0],
                "หมวดหมู่": row[1],
                "เนื้อหา": row[2],
                "สถานะ": row[3]
            })
        
        st.table(display_data)
    else:
        st.info("ยังไม่มีข้อมูลที่บันทึกไว้ในสมุดเล่มนี้")
