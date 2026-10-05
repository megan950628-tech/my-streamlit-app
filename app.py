import streamlit as st

# 設定網頁標題與寬度風格
st.set_page_config(page_title="課程回饋表單", page_icon="📝", layout="centered")

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

gender = st.sidebar.selectbox(
    "性別",
    options=["不願透露", "男", "女", "多元性別"]
)

race = st.sidebar.selectbox(
    "生物/物種型態 (種族)",
    options=[
        "人",
        "學分的狗",
        "水課溺水的魚",
        "一坨爛泥",
        "無魂趕屍人",
        "期末靈魂出竅中",
        "其他神祕物種"
    ]
)

# 使用 st.form 來建立主表單區塊
with st.form("feedback_form"):
    # 1. 姓名 文字輸入欄位
    name = st.text_input("姓名")
    
    # 3. 課程滿意度 1~5 分
    satisfaction = st.slider(
        "課程滿意度 (1 = 非常不滿意，5 = 非常滿意)",
        min_value=1,
        max_value=5,
        value=5
    )
    
    # 4. 意見回饋 文字輸入區
    comments = st.text_area("意見回饋 (選填)")
    
    # 5. 送出按鈕
    submitted = st.form_submit_button("送出")
    
    # 檢查與送出後反應
    if submitted:
        if not name.strip():
            st.error("⚠️ 警告：請填寫您的姓名後再送出！")
        else:
            st.success("感謝您的回饋！")
            
            # 顯示填寫內容摘要
            st.markdown("---")
            st.subheader("📝 您的填寫內容摘要：")
            st.write(f"- **姓名：** {name}")
            st.write(f"- **性別：** {gender}")
            st.write(f"- **科系：** {department}")
            st.write(f"- **物種/種族：** {race}")
            st.write(f"- **滿意度：** {satisfaction} 分")
            if comments:
                st.write(f"- **意見回饋：** {comments}")
