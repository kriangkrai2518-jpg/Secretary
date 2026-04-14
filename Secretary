import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- 1. SETTINGS & STYLE (ความประณีตตามมาตรฐานพี่เกรียง) ---
st.set_page_config(page_title="Personal Secretary V1", page_icon="⭐", layout="wide")

# --- 2. DATABASE ENGINE (ระบบสมุดบันทึกดิจิทัล) ---
def get_db_connection():
    # ใช้ Check same thread เป็น False เพื่อให้รันบน Web Server ได้นิ่ง
    conn = sqlite3.connect('secretary_memory.db', check_same_thread=False)
    return conn

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

# --- 3. UI LOGIC (Interface สำหรับจิตสำนึก) ---
st.title("⭐ Secretary V1: The Identity Keeper")
st.info("เป้าหมาย: รวบรวมความเป็นพี่เกรียง ไม่ให้สูญหายไปตามกาลเวลา")

# Sidebar สำหรับการตั้งค่าหรือกรองข้อมูล
with st.sidebar:
    st.header("⚙️ System Control")
    st.write("User: Kriangkrai (James)")
    mode = st.radio("เลือกโหมด", ["บันทึกตะกอนความคิด", "เรียกคืนความจำ"])

if mode == "บันทึกตะกอนความคิด":
    st.subheader("📥 Input: สิ่งที่ตกตะกอนวันนี้")
    with st.form("identity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("หมวดหมู่การเรียนรู้", 
                                  ["การเทรด (Logic/Strategy)", 
                                   "จิตวิทยา (Mindset/Soul)", 
                                   "ครอบครัว (Legacy/Education)", 
                                   "เทคโนโลยี (Code/AI)"])
        with col2:
            status = st.select_slider("ระดับความสำคัญ", options=["ทั่วไป", "สำคัญ", "กฎเหล็ก/ราชธรรมนูญ"])
        
        content = st.text_area("รายละเอียด (จดลงในจิตใต้สำนึก):")
        
        submit = st.form_submit_button("บันทึกข้อมูลถาวร")
        
        if submit and content:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO legacy_log (timestamp, category, content, status) VALUES (?, ?, ?, ?)",
                      (now, category, content, status))
            conn.commit()
            conn.close()
            st.success("บันทึกสำเร็จ: ข้อมูลถูกจัดเก็บเข้าคลังสมองส่วนขยายเรียบร้อยครับ")

else:
    st.subheader("📖 Retrieval: คลังความจำที่ตกตะกอนแล้ว")
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM legacy_log ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        # ระบบกรองข้อมูล (Jigsaw Organizer)
        filter_cat = st.multiselect("กรองตามหมวดหมู่", df['category'].unique())
        if filter_cat:
            df = df[df['category'].isin(filter_cat)]
        
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("ยังไม่มีชิ้นส่วนจิ๊กซอว์ถูกบันทึกในขณะนี้")
