import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np

# 앱 제목
st.title('📊 생활물가지수 시각화 및 예측')

# CSV 파일 업로드
uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (1열: 연도, 2열: 생활물가지수)", type=["csv"])

if uploaded_file is not None:
    try:
        # 파일 읽기
        df = pd.read_csv(uploaded_file, encoding='cp949')
        st.success("✅ CSV 파일을 성공적으로 불러왔습니다.")
        
        # 열 확인
        if df.shape[1] >= 2:
            df.columns = ['연도', '생활물가지수']

            # 연도 문자열을 정수형 시계열로 변환
            df[['year', 'quarter']] = df['연도'].astype(str).str.split('.', expand=True).astype(int)
            df['numeric_date'] = df['year'] * 4 + df['quarter']

            # 모델 학습
            model = LinearRegression()
            X = df[['numeric_date']]
            y = df['생활물가지수']
            model.fit(X, y)

            # 미래 10년 (40분기) 예측
            last_date = df['numeric_date'].max()
            future_dates = np.arange(last_date + 1, last_date + 41)
            future_preds = model.predict(future_dates.reshape(-1, 1))


            # 시각화
            combined_df = pd.concat([df[['연도', '생활물가지수']], future_df], ignore_index=True)
            fig = px.line(combined_df, x='연도', y='생활물가지수', title='생활물가지수 (실제 + 예측)')
            st.plotly_chart(fig)

            # CSV 다운로드
            csv = future_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(label="📥 예측 결과 CSV 다운로드", data=csv, file_name="예측_생활물가지수.csv", mime='text/csv')

        else:
            st.warning("❗ CSV 파일에는 최소 두 개의 열이 필요합니다.")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
