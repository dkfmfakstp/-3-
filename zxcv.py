import pandas as pd
import plotly.express as px
import streamlit as st

# 앱 제목
st.title('📊 데이터 시각화 웹앱')

# 데이터 초기화
data = None

# Google Drive에서 기본 데이터 불러오기
default_url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"

st.write("기본 데이터셋이 Google Drive에서 자동으로 로드됩니다. 또는 CSV 파일을 업로드할 수 있습니다.")

# CSV 업로드
uploaded_file = st.file_uploader("📁 CSV 파일 업로드", type=["csv"])

# 업로드된 파일이 있으면 해당 데이터 사용, 없으면 기본 데이터 사용
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("✅ 업로드한 CSV 파일을 불러왔습니다.")
    except Exception as e:
        st.error(f"❌ CSV 파일을 읽는 도중 오류가 발생했습니다: {e}")
else:
    try:
        data = pd.read_csv(default_url)
        st.success("✅ Google Drive에서 기본 CSV 파일을 불러왔습니다.")
    except Exception as e:
        st.error(f"❌ 기본 데이터를 불러오는 중 오류가 발생했습니다: {e}")

# 데이터가 있으면 시각화 기능 제공
if data is not None:
    st.write("📋 데이터 미리보기:")
    st.write(data.head())

    # 컬럼 선택
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_columns) >= 2:
        x_axis = st.selectbox("X축 선택", options=numeric_columns, index=0)
        y_axis = st.selectbox("Y축 선택", options=numeric_columns, index=1)

        # 산점도 생성
        fig = px.scatter(data, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
        st.plotly_chart(fig)
    else:
        st.warning("시각화를 위해 최소 2개의 숫자형 열이 필요합니다.")
