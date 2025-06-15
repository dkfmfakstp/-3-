import pandas as pd
import plotly.express as px
import streamlit as st

# 앱 제목
st.title('📊 생활물가지수 시각화')

# 파일 업로드 안내
st.write("CSV 파일을 업로드해주세요. (1열: X축, 2열: Y축)")

# CSV 업로드
uploaded_file = st.file_uploader("📁 CSV 파일 업로드", type=["csv"])

# 업로드한 경우 처리
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("✅ CSV 파일을 성공적으로 불러왔습니다.")
        
        # 열이 2개 이상인지 확인
        if data.shape[1] >= 2:
            x_axis = data.columns[0]
            y_axis = data.columns[1]

            # 그래프 생성
            fig = px.line(data, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
            st.plotly_chart(fig)
        else:
            st.warning("❗ CSV 파일에 최소 두 개의 열이 필요합니다.")
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
