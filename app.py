import streamlit as st

st.set_page_config(page_title="건축가 킴의 부동산 금융 설계기", page_icon="🏠")

# 스타일 설정: 폰트 및 디자인 강화
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 60px; background-color: #eee; border-radius: 10px 10px 0 0; font-weight: bold; font-size: 1.2rem;
    }
    .stTabs [aria-selected="true"] { background-color: #2c3e50 !important; color: white !important; }
    .result-card { 
        background-color: #ffffff; padding: 30px; border-radius: 20px; 
        border: 3px solid #2c3e50; box-shadow: 10px 10px 0px #2c3e50;
        margin-top: 15px;
    }
    .disclaimer { font-size: 0.9rem; color: #888; line-height: 1.6; margin-top: 30px; padding: 15px; background: #f0f0f0; border-radius: 10px; }
    input { font-size: 1.2rem !important; font-weight: 600 !important; }
    label { font-size: 1.1rem !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ 부동산 통합 금융 설계기")

tab1, tab2 = st.tabs(["💰 세금 및 부대비용", "🏦 대출 한도 시뮬레이션"])

# --- [TAB 1: 세금 및 부대비용] ---
with tab1:
    st.subheader("📍 매수 정보 입력")
    price = st.number_input("매매가격 (원)", min_value=0, value=600000000, step=10000000, key="tax_price")
    
    col1, col2 = st.columns(2)
    with col1:
        house_count = st.selectbox("보유 주택 수", ["1주택", "2주택", "3주택 이상"])
        is_first_home = st.checkbox("생애 최초 주택 구입")
    with col2:
        is_adjusted = st.checkbox("조정대상지역 여부")
        is_over_85 = st.checkbox("전용면적 85㎡ 초과")

    # 복비 계산 로직 추가
    def calculate_broker_fee(p):
        if p < 50000000: fee = min(p * 0.006, 250000)
        elif p < 200000000: fee = min(p * 0.005, 800000)
        elif p < 900000000: fee = p * 0.004
        elif p < 1200000000: fee = p * 0.005
        elif p < 1500000000: fee = p * 0.006
        else: fee = p * 0.007
        return fee

    if st.button("🚀 부대비용 계산 시작"):
        # 세율 결정
        if house_count == "1주택":
            rate = 0.01 if price <= 600000000 else (0.02 if price <= 900000000 else 0.03)
        elif house_count == "2주택":
            rate = 0.08 if is_adjusted else 0.01
        else:
            rate = 0.12 if is_adjusted else 0.08
        
        a_tax = price * rate
        if is_first_home: a_tax = max(0, a_tax - 2000000)
        e_tax = a_tax * 0.1
        ag_tax = (price * 0.002) if is_over_85 else 0
        b_fee = calculate_broker_fee(price) # 정밀 복비 계산 적용
        total = a_tax + e_tax + ag_tax + b_fee

        st.markdown(f"""
        <div class="result-card">
            <p style='font-size: 1.3rem; font-weight: 700; color: #666; margin-bottom: 5px;'>📊 예상 부대비용 합계</p>
            <h1 style='color: #d9534f; font-size: 3rem; margin-top: 0; border-bottom: 2px solid #eee; padding-bottom: 10px;'>
                {total:,.0f}<span style='font-size: 1.5rem;'> 원</span>
            </h1>
            <div style='font-size: 1.3rem; line-height: 2.2;'>
                <b>🏠 취득세:</b> {a_tax:,.0f} 원<br>
                <b>└ 지방교육세:</b> {e_tax:,.0f} 원<br>
                <b>└ 농어촌특별세:</b> {ag_tax:,.0f} 원 
                <span style='font-size: 0.9rem; color: #ef5350; font-weight: bold;'>
                    {"(85㎡ 초과 0.2% 부과)" if is_over_85 else "(85㎡ 이하 비과세)"}
                </span><br>
                <b>🤝 예상 중개보수:</b> {b_fee:,.0f} 원
            </div>
            <p style='margin-top: 15px; font-size: 0.95rem; color: #555; background: #f9f9f9; padding: 10px; border-radius: 8px;'>
                💡 <b>건축가 킴의 팁:</b> 전용면적 85㎡를 기준으로 농특세 부과 여부가 결정됩니다. 84㎡ 이하 '국민주택규모' 설계가 세금 측면에서 유리한 이유입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- [TAB 2: 대출 한도 시뮬레이션] ---
with tab2:
    st.subheader("🏦 대출 설계 입력")
    
    col3, col4 = st.columns(2)
    with col3:
        annual_income = st.number_input("연소득 (세전 연봉)", min_value=0, value=50000000, step=1000000)
        loan_period = st.slider("대출 기간 (년)", 10, 40, 30)
    with col4:
        existing_loan_payment = st.number_input("기존 대출 연간 원리금 상환액", min_value=0, value=0)
        interest_rate = st.slider("예상 금리 (%)", 2.0, 8.0, 4.0, 0.1)

    if st.button("🏦 대출 한도 계산 시작"):
        # LTV 70% 계산
        ltv_limit = price * 0.7 
        # DSR 40% 계산 (연소득의 40% - 기존 대출 상환액)
        dsr_limit_annual = (annual_income * 0.4) - existing_loan_payment 
        
        st.markdown(f"""
        <div class="result-card">
            <p style='font-size: 1.3rem; font-weight: 700; color: #666; margin-bottom: 5px;'>📐 예상 대출 가이드라인</p>
            <div style='font-size: 1.4rem; line-height: 2.2;'>
                <p>• <b style='color: #2c3e50;'>LTV 70% 기준 한도:</b><br>
                   <span style='font-size: 2.2rem; color: #2980b9; font-weight: 800;'>{ltv_limit:,.0f} 원</span></p>
                <p>• <b style='color: #2c3e50;'>DSR 40% 기준 연간 상환 가능액:</b><br>
                   <span style='font-size: 2.2rem; color: #27ae60; font-weight: 800;'>{max(0, dsr_limit_annual):,.0f} 원</span></p>
            </div>
            <p style='font-size: 1.1rem; color: #d9534f; font-weight: 700; margin-top: 15px; padding: 10px; border: 1px dashed #d9534f; border-radius: 10px;'>
                ⚠️ 알림: 연간 상환 가능액이 0원이라면, 기존 대출이 소득의 40%를 초과했음을 의미합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 공통 면책 문구 ---
st.markdown(f"""
    <div class="disclaimer">
        <b>[이용 주의사항 및 면책 공고]</b><br>
        1. 본 결과는 최신 세법 및 금융 규정을 바탕으로 설계되었으나, 실제와 차이가 있을 수 있습니다.<br>
        2. 최종 한도는 금융기관의 <b>DSR 심사</b> 결과에 따르며, 은행 방문 상담이 필수입니다.<br>
        3. 건축가 킴은 본 결과에 대해 법적 책임을 지지 않습니다.
    </div>
    <p style='text-align: center; color: #999; margin-top: 20px;'>항상 행운이 함께 하시길!!!</p>
    """, unsafe_allow_html=True)
