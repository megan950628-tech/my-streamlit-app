import streamlit as st
import random
from datetime import datetime
import pandas as pd

# 設定網頁標題與寬度風格
st.set_page_config(page_title="課程回饋表單", page_icon="📝", layout="centered")

# 初始化 session_state 用來暫存多筆回饋紀錄
if "feedback_history" not in st.session_state:
    st.session_state.feedback_history = []

# 頁面說明文字
st.title("📋 課程回饋表單")
st.markdown("""
歡迎填寫本學期的課程回饋表單！您的寶貴意見將有助於我們持續改善教學品質與課程內容。  
請先至左側側邊欄選擇您的基本資訊，並在下方填寫您的體驗與回饋，謝謝您的配合！
""")
st.markdown("---")

# 側邊欄基本資訊設定（科系、性別、種族）
st.sidebar.header("📌 基本資訊設定")

department = st.sidebar.selectbox(
    "所屬科系",
    options=[
        "資訊工程系", 
        "電子工程系", 
        "電機工程系", 
        "資訊管理系", 
        "人工智慧系", 
        "其他"
    ]
)

# 性別選項（已加入「沃爾瑪購物袋」並放在多元性別前面）
gender = st.sidebar.selectbox(
    "性別",
    options=["不願透露", "男", "女", "沃爾瑪購物袋", "多元性別"]
)

race = st.sidebar.selectbox(
    "生物/物種型態 (種族)",
    options=[
        "人",
        "被書砸死的行屍走肉",
        "學分的狗",
        "水課溺水的魚",
        "一坨爛泥",
        "無魂趕屍人",
        "期末靈魂出竅中",
        "其他神祕物種"
    ]
)

# 1. 姓名 文字輸入欄位
name = st.text_input("姓名")

# 3. 課程滿意度 1~5 分（移出 form，拖動時即可即時更新）
satisfaction = st.slider(
    "課程滿意度 (1 = 非常不滿意，5 = 非常滿意)",
    min_value=1,
    max_value=5,
    value=5
)

# 即時狀態提示文字
satisfaction_hints = {
    1: "🥵 這世界怎麼還不爆炸",
    2: "🫠 教授我是小丑放過我",
    3: "🫥 還能活",
    4: "😊 還算充實，學到不少東西",
    5: "🤩 太神啦！直接原地復活"
}
st.info(f"目前狀態預測：{satisfaction_hints[satisfaction]}")

# 4. 意見回饋 文字輸入區
comments = st.text_area("意見回饋 (選填)")
st.caption(f"目前回饋字數：{len(comments)} 字")

# 5. 送出按鈕
submitted = st.button("送出")

# 檢查與送出後反應
if submitted:
    if not name.strip():
        st.error("⚠️ 警告：請填寫您的姓名後再送出！")
    else:
        st.success("感謝您的回饋！")
        
        # 取得當下精確時間
        submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 將資料存入 session_state 歷史紀錄中
        new_entry = {
            "時間": submit_time,
            "姓名": name,
            "性別": gender,
            "科系": department,
            "種族": race,
            "滿意度": satisfaction,
            "意見回饋": comments if comments else "無"
        }
        st.session_state.feedback_history.append(new_entry)
        
        # 隨機產出一句期末金句
        funny_quotes = [
            "「雖然這堂課很累，但我的人生本來就是一場笑話。」",
            "「只要我不尷尬，尷尬的就是期末報告。」",
            "「今天也是努力在延畢邊緣仰式游泳的一天呢！」",
            "「知識有進到腦子裡嗎？沒有，它跟我的髮際線一起走了。」",
            "「感謝老師的授課，讓我成功見證了奇蹟（活到現在）。」"
        ]
        selected_quote = random.choice(funny_quotes)
        
        # 顯示填寫內容摘要
        st.markdown("---")
        st.subheader("📝 您的填寫內容摘要：")
        st.write(f"- **送出時間：** {submit_time}")
        st.write(f"- **姓名：** {name}")
        st.write(f"- **性別：** {gender}")
        st.write(f"- **科系：** {department}")
        st.write(f"- **物種/種族：** {race}")
        st.write(f"- **滿意度：** {satisfaction} 分")
        if comments:
            st.write(f"- **意見回饋：** {comments}")
            
        st.markdown("---")
        st.markdown(f"💡 **今日語錄：** *{selected_quote}*")

# 實用功能區：若已有送出紀錄，在下方提供 CSV 檔案下載按鈕與表格預覽
if st.session_state.feedback_history:
    st.markdown("---")
    st.subheader("📊 管理員專區：回饋數據匯出")
    df = pd.DataFrame(st.session_state.feedback_history)
    st.dataframe(df, use_container_width=True)
    
    # 轉換為 CSV 供下載
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載所有回饋紀錄 (CSV)",
        data=csv_data,
        file_name=f"course_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
