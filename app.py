import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np

# 앱 제목
st.title('📊 생할물가지수 시각화 + 예측')

# 파일 업로드 안내
st.write("CSV 파일을 업로드해주세요. (1열: 년도.분기, 2열: 생할물가지수)")

# CSV 업로드
uploaded_file = st.file_uploader("📁 CSV 파일 업로드", type=["csv"])

# 업로드한 경우 처리
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file, encoding='cp949')
        st.success("✅ CSV 파일을 성공적으로 끌어왔습니다.")

        # 열이 2개 이상인지 확인
        if data.shape[1] >= 2:
            x_col = data.columns[0]
            y_col = data.columns[1]

            # 그래프 생성
            fig = px.line(data, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
            st.plotly_chart(fig)

            # 예측 후 더트리언 생성
            st.subheader("✨ 예측 결과 (다음 10년)")

            # 값 수치화되지 않은 경우 처리
            df = data[[x_col, y_col]].copy()
            df.columns = ['date', 'index']

            # 년도.분기 문자열을 수치로 변환 (ex: 1995.1 -> 1995.0, 1995.4 -> 1995.75)
            df['numeric_date'] = df['date'].astype(str).str.extract(r'(\d{4})\.(\d)').astype(float)
            df['numeric_date'] = df['numeric_date'][0] + (df['numeric_date'][1] - 1) * 0.25

            # 데이터 형태 검사
            df.dropna(inplace=True)
            X = df[['numeric_date']].values
            y = df['index'].values

            # 선형 행렬 형식 통계 문으로 환샜
            model = LinearRegression()
            model.fit(X, y)

            # 다음 10년간 40분기 예측
            last = df['numeric_date'].max()
            future_dates = np.array([last + 0.25 * i for i in range(1, 41)])
            future_preds = model.predict(future_dates.reshape(-1, 1))

            # 예측 결과 보유
            future_df = pd.DataFrame({
                'date': [f"{int(d)}.{int((d%1)*4+1)}" for d in future_dates],
                'index': future_preds
            })

            # 열랍기 기준 각종 결과
            total_df = pd.concat([df[['date', 'index']], future_df], ignore_index=True)
            fig2 = px.line(total_df, x='date', y='index', title="생할물가지수 (기초+예측)")
            st.plotly_chart(fig2)

        else:
            st.warning("❗ CSV 파일에 최소 두 개의 열이 필요합니다.")
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
