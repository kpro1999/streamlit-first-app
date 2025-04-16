import datetime
import streamlit as st
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt # Plotly 사용 시 필요 없음
# import matplotlib.dates as mdates # Plotly 사용 시 필요 없음
import plotly.graph_objects as go # Plotly import 추가

# 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="First Streamlit App", layout="wide")

st.title(f"공장 효율 분석")
st.write("이 앱은 공장 효율을 분석하는 데 사용됩니다.")

# --- 날짜 입력 ---
d = st.date_input("확인할 날짜", "today")
st.write("현재 보여지는 데이터는 날짜:", d)

st.subheader("사용량 표시", divider=True)
cc = st.columns(3)

# --- 물 사용량 데이터 생성 ---
end_date = d
start_date = end_date - datetime.timedelta(days=30) # 예시: 총 7일 데이터
# freq='D' 명시 권장
dates = pd.date_range(start=start_date, end=end_date, freq='D')
# dates_d = pd.Index(dates.values.astype('datetime64[D]')) # 이 줄은 필요 없음
water_usage = np.random.randint(800, 1500, size=len(dates))

# DataFrame 생성 시 원래 DatetimeIndex(dates) 사용
water_usage_data = pd.DataFrame({'사용량(m³)': water_usage}, index=dates)

# 인덱스를 문자열로 변경하는 코드 제거 (Plotly에서 DatetimeIndex 직접 사용)
# water_usage_data.index = dates.strftime('%m/%d') # <--- 이 줄 제거
# print(dates_d) # 제거

water_usage_data.index.name = '날짜' # 인덱스 이름 설정

# --- 메트릭 표시 ---
# 메트릭은 마지막 날짜 기준이므로 인덱스 타입 변경과 무관
last_day_usage = water_usage_data['사용량(m³)'].iloc[-1]
delta_usage = np.random.randint(-100, 101)
cc[0].metric(label="물 사용량",
             value=f"{last_day_usage} m³",
             delta=f"{delta_usage} m³",
             delta_color="inverse" if delta_usage < 0 else "normal",
             help=f"{d} 기준 전일 대비 물 사용량 변화량",
             border=True)
cc[1].metric(label="전기 사용량", value="8,500 kWh", delta="-200 kWh")
cc[2].metric(label="가스 사용량", value="350 m³", delta="15 m³")

# --- 차트 섹션 ---
ccChart = st.columns(3)

# --- 물 사용량 차트 (ccChart[0]) - Plotly 사용 및 초기 범위 설정 ---

# 초기 화면에 표시할 최근 일수 정의
initial_days_to_show = 10 # 예시: 최근 5일

# 초기 표시 시작 날짜 계산 (전체 데이터가 5일 미만일 경우 고려)
if len(dates) >= initial_days_to_show:
    initial_start_date = end_date - datetime.timedelta(days=initial_days_to_show - 1)
else:
    initial_start_date = start_date # 데이터가 적으면 처음부터 보여줌

# Plotly Figure 생성
fig_water = go.Figure()
# 전체 데이터를 사용하여 막대 추가
fig_water.add_trace(go.Bar(
    x=water_usage_data.index, # DatetimeIndex 사용
    y=water_usage_data['사용량(m³)'],
    name='물 사용량',
    width=1, # 막대 굵기 (선택 사항)
    marker_color='rgb(26, 118, 255)',
    hovertemplate='<b>날짜</b>: %{x|%Y/%m/%d}<br>' + # 툴팁 형식
                  '<b>사용량</b>: %{y} m³' +
                  '<extra></extra>'
))
# 차트 레이아웃 업데이트
fig_water.update_layout(
    xaxis_title='날짜',
    yaxis_title='사용량(m³)',
    bargap=0.1,
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis_tickformat='%m/%d', # X축 눈금 형식 ('%Y/%m/%d' 등 원하는 대로)
    # --- 초기 X축 표시 범위 설정 ---
    xaxis_range=[initial_start_date, end_date] # <--- 이 부분 추가
)

# 생성된 Plotly 차트를 Streamlit 컬럼[0]에 표시
# ccChart[0].plotly_chart(fig_water, use_container_width=True)
# --- 물 사용량 차트 끝 ---

x = water_usage_data.index.strftime('%y/%m/%d').values
y = water_usage_data['사용량(m³)'].values
# Use textposition='auto' for direct text
fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
ccChart[0].plotly_chart(fig, use_container_width=True)


# --- 전기 및 가스 차트 (기존 st.bar_chart 유지 또는 Plotly로 변경 가능) ---
# 예시: 전기 사용량 차트 (st.bar_chart)
elec_usage = np.random.randint(7000, 9500, size=len(dates))
elec_data = pd.DataFrame({'사용량(kWh)': elec_usage}, index=dates)
elec_data.index.name = '날짜'
ccChart[1].bar_chart(
    data=elec_data,
    use_container_width=True,
    width=0.9, # 막대 굵기 조절 (0 ~ 1 사이, 0.7 정도가 적당할 수 있음)
)
# 예시: 가스 사용량 차트 (st.bar_chart)
gas_usage = np.random.randint(300, 500, size=len(dates))
gas_data = pd.DataFrame({'사용량(m³)': gas_usage}, index=dates)
gas_data.index.name = '날짜'
ccChart[2].bar_chart(
    data=gas_data,
    use_container_width=True,
)

# 간격 추가
for i in range(3):
    st.markdown("")

st.subheader("작업량", divider=True)

# 작업량 메트릭 컨테이너
with st.container():
  a, b = st.columns(2)
  c, d = st.columns(2)
  a.metric("**수건**", "1000 KG", "-100 KG", delta_color="inverse", border=True)
  b.metric("**침대보**", "945 개", "-5 개", delta_color="inverse", border=True)
  c.metric("총 무게", "3000 KG", "100 KG", delta_color="inverse", border=True)
