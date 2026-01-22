import streamlit as st

st.set_page_config(page_title="건축가 킴의 부동산 세금 설계기", page_icon="🏠")

# 스타일 업그레이드
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stNumberInput, .stSelectbox { border: 2px solid #2c3e50; }
    .result-card { 
        background-color: #ffffff; padding: 25px; border-radius: 20px; 
        border: 3px solid #2c3e50; box-shadow: 8px 8px 0px #2c3e50;
        margin-top: 20px;
    }
    .tax-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #eee; }
    .total-row { font-size: 1.4rem; font-weight: 800; color: #d9534f; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ 부동산 매수 총비용 설계기")
st.caption("취득세부터 중개수수료까지, 건축가가 설계하는 실무 데이터")

# --- 입력 섹션 ---
with st.expander("📍 기본 정보 입력", expanded=True):
    price = st.number_input("매매가격 (원)", min_value=0, value=600000000, step=10000000)
    
    col1, col2 = st.columns(2)
    with col1:
        house_count = st.selectbox("보유 주택 수", ["1주택", "2주택", "3주택 이상"])
        is_first_home = st.checkbox("생애 최초 주택 구입인가요?")
    with col2:
        is_adjusted = st.checkbox("조정대상지역 여부")
        is_over_85 = st.checkbox("전용면적 85㎡ 초과인가요?")

# --- 확장 계산 로직 ---
def get_detailed_tax(price, count, adjusted, first_home, over_85):
    # 1. 기본 취득세율 (본세)
    if count == "1주택":
        if price <= 600000000: rate = 0.01
        elif price <= 900000000: rate = (price * 2 / 300000000) - 3 / 100
        else: rate = 0.03
    elif count == "2주택":
        rate = 0.08 if adjusted else (0.01 if price <= 600000000 else 0.03) # 간소화
    else:
        rate = 0.12 if adjusted else 0.08
    
    acquisition_tax = price * rate
    
    # 2. 생애최초 감면 (최대 200만원 한도)
    discount = 0
    if first_home:
        discount = min(acquisition_tax, 2000000)
        acquisition_tax -= discount

    # 3. 부가세 (지방교육세, 농특세)
    edu_tax = acquisition_tax * 0.1 # 본세의 10% 기준
    agri_tax = (price * 0.002) if over_85 else 0 # 85㎡ 초과시 농특세 발생
    
    # 4. 중개수수료 (0.4%~0.9% 구간 적용)
    if price < 50000000: commission_rate = 0.006
    elif price < 200000000: commission_rate = 0.005
    elif price < 900000000: commission_rate = 0.004
    else: commission_rate = 0.005
    broker_fee = price * commission_rate

    return acquisition_tax, edu_tax, agri_tax, discount, broker_fee

# --- 결과 출력 ---
if st.button("🚀 총 소요비용 시뮬레이션 시작"):
    a_tax, e_tax, ag_tax, disc, b_fee = get_detailed_tax(price, house_count, is_adjusted, is_first_home, is_over_85)
    total_cost = a_tax + e_tax + ag_tax + b_fee
    
    st.markdown(f"""
    <div class="result-card">
        <div class="tax-row"><span>취득세 (본세)</span><span>{a_tax:,.0f}원</span></div>
        <div class="tax-row"><span>지방교육세</span><span>{e_tax:,.0f}원</span></div>
        <div class="tax-row"><span>농어촌특별세</span><span>{ag_tax:,.0f}원</span></div>
        <div class="tax-row" style="color: #27ae60;"><span>🎁 생애최초 감면액</span><span>- {disc:,.0f}원</span></div>
        <div class="tax-row"><span>예상 중개수수료 (복비)</span><span>{b_fee:,.0f}원</span></div>
        <div class="tax-row total-row">
            <span>총 부대비용</span>
            <span>{total_cost:,.0f}원</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"💡 주택 매수 시 실제 필요한 총 현금(매매가 포함)은 약 **{(price + total_cost):,.0f}원** 입니다.")
