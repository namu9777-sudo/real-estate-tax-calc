import streamlit as st

# 페이지 설정
st.set_page_config(page_title="건축가 킴의 부동산 세금 설계기", page_icon="🏠")

# CSS: 전문적인 느낌을 주는 스타일
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stNumberInput, .stSelectbox { border: 1px solid #333; }
    .result-box { 
        background-color: #ffffff; padding: 20px; border-radius: 15px; 
        border: 2px solid #333; box-shadow: 5px 5px 0px #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏠 부동산 취득세 계산기")
st.caption("건축가의 시각으로 정밀하게 설계하는 취득세 시뮬레이션")

# --- 입력 섹션 ---
with st.container():
    st.subheader("📍 매수 정보 입력")
    price = st.number_input("매매가격을 입력하세요 (원)", min_value=0, value=600000000, step=10000000)
    
    col1, col2 = st.columns(2)
    with col1:
        house_count = st.selectbox("보유 주택 수 (취득 포함)", ["1주택", "2주택", "3주택 이상"])
    with col2:
        is_adjusted = st.checkbox("조정대상지역 여부")

# --- 계산 엔진 (기초 로직) ---
def calculate_tax(price, count, adjusted):
    # 2024년 주택 취득세율 간소화 로직
    if count == "1주택":
        if price <= 600000000: rate = 0.01
        elif price <= 900000000: rate = (price * 2 / 300000000) - 3 / 100 # 수식 적용
        else: rate = 0.03
    elif count == "2주택":
        rate = 0.08 if adjusted else 0.01 # 비조정 2주택은 일반세율
    else:
        rate = 0.12 if adjusted else 0.08
    return rate

# --- 결과 출력 ---
if st.button("💰 세금 설계 시작"):
    rate = calculate_tax(price, house_count, is_adjusted)
    main_tax = price * (rate if rate > 0.01 else 0.01)
    
    st.markdown("---")
    st.markdown(f"""
    <div class="result-box">
        <h2 style='color: #111; margin-top:0;'>📊 예상 취득세액</h2>
        <h1 style='color: #d9534f;'>약 {main_tax:,.0f} 원</h1>
        <p style='color: #666;'>적용 세율: {rate*100:.2f}% (기본세율 기준)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 지방교육세 및 농어촌특별세는 별도로 부과될 수 있습니다.")
    st.warning("⚠️ 본 결과는 참고용이며, 정확한 세액은 세무사 등 전문가와 상의하십시오.")

st.markdown('<p style="text-align: center; color: #999; margin-top: 50px;">로또는 소액으로 즐기면서 하세요!!!</p>', unsafe_allow_html=True)
