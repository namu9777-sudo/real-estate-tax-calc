import streamlit as st

st.set_page_config(page_title="건축가 킴의 부동산 금융 설계기", page_icon="🏠")

# 1. 스타일 설정
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #eee; border-radius: 10px 10px 0 0; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #2c3e50 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ 부동산 통합 금융 설계기")

tab1, tab2 = st.tabs(["💰 세금 및 부대비용", "🏦 대출 한도 시뮬레이션"])

# --- [TAB 1: 세금 계산기] ---
with tab1:
    st.subheader("📍 매수 정보 입력")
    price = st.number_input("매매가격 (원)", min_value=0, value=600000000, step=10000000, key="tax_p")
    
    col1, col2 = st.columns(2)
    with col1:
        house_count = st.selectbox("보유 주택 수", ["1주택", "2주택", "3주택 이상"])
        is_first_home = st.checkbox("생애 최초 주택 구입")
    with col2:
        is_adjusted = st.checkbox("조정대상지역 여부")
        is_over_85 = st.checkbox("전용면적 85㎡ 초과")

    # 계산 함수
    def get_detailed_tax(p, c, a, f, o):
        if c == "1주택":
            rate = 0.01 if p <= 600000000 else (0.02 if p <= 900000000 else 0.03)
        elif c == "2주택":
            rate = 0.08 if a else 0.01
        else:
            rate = 0.12 if a else 0.08
        
        a_tax = p * rate
        if f: a_tax = max(0, a_tax - 2000000) # 감면 적용
        
        e_tax = a_tax * 0.1
        ag_tax = (p * 0.002) if o else 0
        b_fee = p * 0.004
        return a_tax, e_tax, ag_tax, b_fee

    if st.button("🚀 부대비용 계산"):
        a, e, ag, b = get_detailed_tax(price, house_count, is_adjusted, is_first_home, is_over_85)
        total = a + e + ag + b
        
        # 디자인 렌더링 (이 부분이 핵심입니다!)
        result_html = f"""
        <div style="background-color: #ffffff; padding: 30px; border-radius: 20px; border: 3px solid #2c3e50; box-shadow: 10px 10px 0px #2c3e50; margin-top: 20px;">
            <p style='margin: 0; font-size: 1.2rem; color: #666; font-weight: 700;'>📊 예상 총 소요 비용</p>
            <h1 style='margin: 15px 0; color: #d9534f; font-size: 3rem; border-bottom: 3px solid #eee; padding-bottom: 20px; font-weight: 900;'>
                {total:,.0f}<span style='font-size: 1.8rem;'> 원</span>
            </h1>
            <div style='margin-top: 25px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 15px;'>
                    <span style='font-size: 1.5rem; font-weight: 800;'>🏠 취득세(본세)</span>
                    <span style='font-size: 1.5rem; font-weight: 800;'>{a:,.0f} 원</span>
                </div>
                <div style='display: flex; justify-content: space-between; color: #444; margin-bottom: 10px;'>
                    <span style='font-size: 1.3rem; font-weight: 600;'>└ 지방교육세</span>
                    <span style='font-size: 1.3rem; font-weight: 600;'>{e:,.0f} 원</span>
                </div>
                <div style='display: flex; justify-content: space-between; color: #444; margin-bottom: 10px;'>
                    <span style='font-size: 1.3rem; font-weight: 600;'>└ 농어촌특별세</span>
                    <span style='font-size: 1.3rem; font-weight: 600;'>{ag:,.0f} 원</span>
                </div>
                <div style='display: flex; justify-content: space-between; color: #2980b9; margin-top: 20px; padding-top: 15px; border-top: 2px dashed #ccc;'>
                    <span style='font-size: 1.4rem; font-weight: 800;'>🤝 예상 중개수수료</span>
                    <span style='font-size: 1.4rem; font-weight: 800;'>{b:,.0f} 원</span>
                </div>
            </div>
        </div>
        """
        # 반드시 unsafe_allow_html=True를 넣어야 합니다.
        st.markdown(result_html, unsafe_allow_html=True)

# --- [TAB 2: 대출 한도] ---
with tab2:
    st.subheader("🏦 대출 설계 가이드")
    income = st.number_input("연소득 (원)", min_value=0, value=50000000, key="inc")
    loan_rate = st.slider("예상 금리 (%)", 2.0, 8.0, 4.0, 0.1)
    
    st.info("💡 대출 한도 계산 로직을 준비 중입니다. (DSR 가이드 예정)")

# 공통 면책 문구
st.markdown("<br><p style='font-size: 0.8rem; color: #888;'>※ 본 결과는 참고용이며 실제와 다를 수 있습니다.</p>", unsafe_allow_html=True)
