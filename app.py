import streamlit as st
import random
from datetime import datetime
import pandas as pd
from collections import Counter
import re
import altair as alt

# 設定網頁標題與寬度風格
st.set_page_config(page_title="課程回饋表單", page_icon="📝", layout="centered")

# 溫和質感的按鈕自訂 CSS
st.markdown("""
<style>
div.stButton > button {
    background-color: #f0f2f6;
    color: #31333F;
    border: 1px solid #d6d6d8;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 16px;
    font-weight: 500;
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    background-color: #e2e4e9;
    border-color: #b0b3bc;
    color: #000000;
    transform: translateY(-1px);
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# 初始化 session_state
if "feedback_history" not in st.session_state:
    st.session_state.feedback_history = []

if "satisfaction" not in st.session_state:
    st.session_state.satisfaction = None

# 頁面說明文字
st.title("📋 課程回饋表單")
st.markdown("""
歡迎填寫本學期的課程回饋表單！您的寶貴意見將有助於我們持續改善教學品質與課程內容。  
請在下方依序填寫您的基本資訊與課程回饋，謝謝您的配合！
""")
st.markdown("---")

# 📌 基本資訊設定（初始預設為「請選擇」）
st.subheader("📌 基本資訊設定")

department = st.selectbox(
    "所屬科系",
    options=["請選擇", "資訊工程系", "電子工程系", "電機工程系", "資訊管理系", "人工智慧系", "其他"]
)

gender = st.selectbox(
    "性別",
    options=["請選擇", "不願透露", "男", "女", "沃爾瑪購物袋", "多元性別"]
)

race = st.selectbox(
    "生物/物種型態 (種族)",
    options=["請選擇", "人", "被書砸死的行屍走肉", "學分的狗", "水課溺水的魚", "一坨爛泥", "無魂趕屍人", "期末靈魂出竅中", "其他神祕物種"]
)

# 種族專屬評價對照字典
race_evaluations = {
    "人": "還有高手?",
    "被書砸死的行屍走肉": "一路走好",
    "學分的狗": "汪汪",
    "水課溺水的魚": "教授，撈撈",
    "一坨爛泥": "來台回收車收了我",
    "無魂趕屍人": "快跑",
    "期末靈魂出竅中": "那還說啥了，我直接跳了",
    "其他神祕物種": "有待發現......"
}

# 即時顯示種族評價
if race != "請選擇":
    st.caption(f"🧬 物種評語：{race_evaluations[race]}")

st.markdown("---")
st.subheader("📝 意見回饋與評分")

# 1. 姓名 文字輸入欄位
name = st.text_input("姓名")

# 3. 課程滿意度：保持按鈕狀
st.write("課程滿意度 (1 = 非常不滿意，5 = 非常滿意)")
cols = st.columns(5)
score_labels = {
    1: "1 🥵",
    2: "2 🫠",
    3: "3 🫥",
    4: "4 😊",
    5: "5 🤩"
}

for i, score in enumerate([1, 2, 3, 4, 5]):
    with cols[i]:
        if st.button(score_labels[score], key=f"sat_btn_{score}", use_container_width=True):
            st.session_state.satisfaction = score

satisfaction = st.session_state.satisfaction

# 即時狀態提示文字
if satisfaction is not None:
    satisfaction_hints = {
        1: "🥵 這世界怎麼還不爆炸",
        2: "🫠 教授我是小丑放過我",
        3: "🫥 還能活",
        4: "😊 還算充實，學到不少東西",
        5: "🤩 太神啦！直接原地復活"
    }
    st.info(f"目前狀態預測：{satisfaction_hints[satisfaction]}")
else:
    st.info("目前狀態預測：請點選上方滿意度按鈕進行評分")

# 4. 意見回饋 文字輸入區（即時字數統計）
comments = st.text_area("意見回饋 (選填)")
st.caption(f"目前回饋字數：{len(comments)} 字")

# 5. 送出按鈕
submitted = st.button("送出")

# 檢查與送出後反應（加入完整的未選擇防呆檢查）
if submitted:
    missing_fields = []
    if not name.strip():
        missing_fields.append("姓名")
    if department == "請選擇":
        missing_fields.append("所屬科系")
    if gender == "請選擇":
        missing_fields.append("性別")
    if race == "請選擇":
        missing_fields.append("生物/物種型態 (種族)")
    if satisfaction is None:
        missing_fields.append("課程滿意度")

    if missing_fields:
        st.error(f"⚠️ 警告：以下欄位尚未完整填寫或選擇：{', '.join(missing_fields)}！")
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
            "種族評價": race_evaluations[race],
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
        st.write(f"- **物種/種族：** {race} （評語：{race_evaluations[race]}）")
        st.write(f"- **滿意度：** {satisfaction} 分")
        if comments:
            st.write(f"- **意見回饋：** {comments}")
            
        st.markdown("---")
        st.markdown(f"💡 **今日語錄：** *{selected_quote}*")

# 📊 統計儀表板與數據專區（僅在有回饋資料時顯示）
df = pd.DataFrame(st.session_state.feedback_history)

if len(df) > 0:
    st.markdown("---")
    st.subheader("📊 管理員專區：回饋數據與分析儀表板")

    # 1. 科系統計與情感傾向圓餅圖（統一高度）
    c_col1, c_col2 = st.columns(2)

    with c_col1:
        st.write("**📌 各科系填寫比例 (圓餅圖)**")
        dept_counts = df["科系"].value_counts().reset_index()
        dept_counts.columns = ["科系", "數量"]
        
        pie_dept = alt.Chart(dept_counts).mark_arc(outerRadius=80).encode(
            theta=alt.Theta(field="數量", type="quantitative"),
            color=alt.Color(field="科系", type="nominal"),
            tooltip=['科系', '數量']
        ).properties(height=220)
        st.altair_chart(pie_dept, use_container_width=True)

    with c_col2:
        st.write("**📌 情感傾向分佈 (圓餅圖)**")
        def get_sentiment(sat):
            if sat >= 4:
                return "正面 😊"
            elif sat == 3:
                return "中立 🫥"
            else:
                return "負面 🥵"
        df_temp = df.copy()
        df_temp["情感傾向"] = df_temp["滿意度"].apply(get_sentiment)
        sentiment_counts = df_temp["情感傾向"].value_counts().reset_index()
        sentiment_counts.columns = ["情感傾向", "數量"]
        
        pie_sent = alt.Chart(sentiment_counts).mark_arc(outerRadius=80).encode(
            theta=alt.Theta(field="數量", type="quantitative"),
            color=alt.Color(field="情感傾向", type="nominal", scale=alt.Scale(domain=["正面 😊", "中立 🫥", "負面 🥵"], range=["#48bb78", "#ecc94b", "#f56565"])),
            tooltip=['情感傾向', '數量']
        ).properties(height=220)
        st.altair_chart(pie_sent, use_container_width=True)

    # 2. 情感傾向與互斥不重複關鍵字前三名
    st.markdown("---")
    st.subheader("💬 各情感傾向互斥熱門關鍵字 Top 3")
    
    sentiments = ["正面 😊", "中立 🫥", "負面 🥵"]
    used_words = set()
    sentiment_keywords = {}
    
    for sent in sentiments:
        if sent == "正面 😊":
            sub_df = df[df["滿意度"] >= 4]
        elif sent == "中立 🫥":
            sub_df = df[df["滿意度"] == 3]
        else:
            sub_df = df[df["滿意度"] <= 2]
            
        all_text = " ".join(sub_df[sub_df["意見回饋"] != "無"]["意見回饋"].tolist())
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', all_text)
        word_counts = Counter(words).most_common()
        
        unique_top3 = []
        for word, count in word_counts:
            if word not in used_words:
                unique_top3.append((word, count))
                used_words.add(word)
            if len(unique_top3) == 3:
                break
        sentiment_keywords[sent] = unique_top3

    kw_cols = st.columns(3)
    for idx, sent in enumerate(sentiments):
        with kw_cols[idx]:
            st.markdown(f"**{sent} 關鍵字 Top 3**")
            top3 = sentiment_keywords[sent]
            if top3:
                for w, c in top3:
                    st.write(f"- {w} ({c}次)")
            else:
                st.write("- 無資料")

    # 3. 完整原始資料表格預覽
    st.markdown("---")
    st.write("**📋 所有回饋紀錄明細**")
    st.dataframe(df, use_container_width=True, height=220)
    
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載所有回饋紀錄 (CSV)",
        data=csv_data,
        file_name=f"course_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
