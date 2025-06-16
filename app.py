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
        if df.shape[1] >= 2:        #열이 2개 이상이면
            df.columns = ['연도', '생활물가지수']     #열에 '연도'와 '생활물가지수'이름 부여

            # 연도 문자열을 정수형 시계열로 변환
            df[['year', 'quarter']] = df['연도'].astype(str).str.split('.', expand=True).astype(int)  #연도 문자열을 '.'을 기준으로 'year'와 'quater'로 나눈다.
            df['numeric_date'] = df['year'] * 4 + df['quarter']        #'year'*4+1을 하여 정수형 시계열로 변환하고 이를 저장장

            # 모델 학습
            model = LinearRegression()    #선형 회귀 예측 모델 불러오기
            X = df[['numeric_date']]       #x축에 정수형 시계열 적용
            y = df['생활물가지수']      #y축에 생활물가지수 적용
            model.fit(X, y)      #입력된 정보를 토대로 예측하고 예측값 만들기

            # 미래 10년 (40분기) 예측
            last_date = df['numeric_date'].max()      #마지막 정수형 시계열(최댓값)을 찾는다.
            future_dates = np.arange(last_date + 1, last_date + 41)     #이후 1부터 41까지 최댓값에 더해 40개의 정수형 시계열을 만든다.
            future_preds = model.predict(future_dates.reshape(-1, 1))       #만든 40개의 정수형 시계열을 2차원 리스트로 만들어 해당 공간에 예측값을 저장한다.

            
            # 연도.분기 형식으로 변환
            future_years = future_dates // 4       #정수형 시계열을 4로 나누고 연도에 저장
            future_quarters = future_dates % 4 + 1       #정수형 시계열의 나머지를 찾고 +1을 하여 분기에 저장 예:(나머지가 0이면 1분기)
            future_labels = future_years.astype(str) + '.' + future_quarters.astype(str)   #연도와 분기를 '.'을 사이에 두고 저장

            future_df = pd.DataFrame({
                '연도': future_labels,       #저장한 연도와 분기를 '연도'에 저장
                '생활물가지수': future_preds      #저장한 40개의 예측값을 '생활물가지수'에 저장
            })


            # 시각화
            combined_df = pd.concat([df[['연도', '생활물가지수']], future_df], ignore_index=True)    #기존의 csv파일에 있던 정보 아래에 연도와 예측값 추가
            fig = px.line(combined_df, x='연도', y='생활물가지수', title='생활물가지수 (실제 + 예측)')       #정보를 토대로 꺾은선 그래프 제작
            st.plotly_chart(fig)   #만들어진 그래프 시각화

            # CSV 다운로드
            csv = csv = future_df.to_csv(index=False, encoding='cp949')    #예측값을 csv파일로 변환하여 저장
            st.download_button(label="📥 예측 결과 CSV 다운로드", data=csv, file_name="예측_생활물가지수.csv", mime='text/csv')    #파일을 다운로드 할 수 있는 버튼


        else:
            st.warning("❗ CSV 파일에는 최소 두 개의 열이 필요합니다.")     #열이 2개 이상이 아닐경우


    except Exception as e:
        st.error("❌ 오류 발생")   #과정에서 오류가 발생할 경우
