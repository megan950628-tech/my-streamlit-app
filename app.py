import streamlit as st

# 設定網頁標題
st.title("📋 課程回饋表單")
st.write("請填寫以下表單，協助我們持續改善課程品質！")

# 使用 st.form 來建立表單區塊，讓送出體驗更流暢
with st.form("feedback_form"):
    # 1. 姓名 文字輸入欄位
    name = st.text_input("姓名")
    
    # 2. 科系 下拉式選單
    department = st.selectbox(
        "科系",
        options=["資訊工程系", "電子工程系", "其他"]
    )
    
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
    
    # 6. 按下送出後顯示「感謝您的回饋！」
    if submitted:
        if not name.strip():
            st.error("請填寫您的姓名後再送出！")
        else:
            st.success("感謝您的回饋！")
            
            # (選擇性) 顯示填寫內容摘要
            st.markdown("---")
            st.subheader("📝 您的填寫內容摘要：")
            st.write(f"- **姓名：** {name}")
            st.write(f"- **科系：** {department}")
            st.write(f"- **滿意度：** {satisfaction} 分")
            if comments:
                st.write(f"- **意見回饋：** {comments}")
