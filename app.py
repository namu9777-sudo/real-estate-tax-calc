import streamlit as st

st.set_page_config(page_title="건축가 킴의 부동산 금융 설계기", page_icon="🏠")

# 스타일 업그레이드 (카드 디자인 및 탭 스타일)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #eee;
        border-radius: 10px 10px 0 0; gap: 1px; padding: 10px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #2c3e50 !important; color: white !important; }
    .result-card { 
        background-color: #ffffff; padding: 25px; border-radius: 20px; 
        border: 3px solid #2c3e50; box-shadow: 8px 8px 0px #2c3e50;
        margin-top: 10px;
    }
    .disclaimer { font-size: 0.8rem; color: #888; line-height: 1.5; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ 부동산 통합 금융 설계기")

# 탭 구성: 세금 계산과 대출 설계를 분리
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

    # 계산 로직 (기존과 동일)
    def get_detailed_tax(p, c, a, f, o):
        if c == "1주택":
            rate = 0.01 if p <= 600000000 else (0.02 if p <= 900000000 else 0.03)
        elif c == "2주택":
            rate = 0.08 if a else 0.01
        else:
            rate = 0.12 if a else 0.08
        
        a_tax = p * rate
        if f: a_tax = max(0, a_tax - 2000000) # 생애최초 감면
        
        e_tax = a_tax * 0.1
        ag_tax = (p * 0.002) if o else 0
        b_fee = p * 0.004 # 평균 요율 적용
        return a_tax, e_tax, ag_tax, b_fee

    if st.button("🚀 부대비용 계산"):
        a, e, ag, b = get_detailed_tax(price, house_count, is_adjusted, is_first_home, is_over_85)
        total = a + e + ag + b
        st.markdown(f"""
        <div class="result-card">
            <h3>📊 예상 부대비용 합계</h3>
            <h2 style='color: #d9534f;'>약 {total:,.0f} 원</h2>
            <p style='font-size: 0.9rem;'>취득세 {a:,.0f} / 교육세 {e:,.0f} / 농특세 {ag:,.0f} / 복비 {b:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

# --- [TAB 2: 대출 한도 시뮬레이션] ---
with tab2:
    st.subheader("🏦 대출 설계 입력")
    st.write("사용자의 소득과 LTV를 기준으로 가이드라인을 산출합니다.")
    
    col3, col4 = st.columns(2)
    with col3:
        annual_income = st.number_input("연소득 (세전 연봉)", min_value=0, value=50000000, step=1000000)
        loan_period = st.slider("대출 기간 (년)", 10, 40, 30)
    with col4:
        existing_loan_payment = st.number_input("기존 대출 연간 원리금 상환액", min_value=0, value=0)
        interest_rate = st.slider("예상 대출 금리 (%)", 2.0, 8.0, 4.0, 0.1)

    # 단순 LTV/DSR 가이드 계산
    ltv_limit = price * 0.7 # 비조정 기준 70%
    dsr_limit_annual = (annual_income * 0.4) - existing_loan_payment # DSR 40% 적용
    
    st.markdown(f"""
    <div class="result-card">
        <h3>📐 예상 대출 가이드라인</h3>
        <p>• <b>LTV 70% 기준 한도:</b> {ltv_limit:,.0f} 원</p>
        <p>• <b>DSR 40% 기준 연간 상환 가능액:</b> {max(0, dsr_limit_annual):,.0f} 원</p>
        <p style='font-size: 0.85rem; color: #555;'>※ 위 금액은 단순 참고용이며, 실제 심사 시 소득 증빙 방식과 은행별 기준에 따라 크게 달라질 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 공통 면책 문구 (Bottom) ---
st.markdown(f"""
    <div class="disclaimer">
        <b>[이용 주의사항 및 면책 공고]</b><br>
        1. 본 시뮬레이션 결과는 최신 세법 및 금융 규정을 바탕으로 제작되었으나, 개별 상황에 따라 실제 금액과 차이가 발생할 수 있습니다.<br>
        2. 대출 가능 여부와 최종 한도는 금융기관의 <b>DSR(총부채원리금상환비율) 심사</b> 결과에 따라 결정됩니다.<br>
        3. 정확한 세액 및 대출 한도는 반드시 세무사, 법무사 및 은행 창구를 통해 확인하시기 바랍니다.<br>
        4. 건축가 킴은 본 결과에 대해 법적 책임을 지지 않습니다.
    </div>
    """, unsafe_allow_html=True)
