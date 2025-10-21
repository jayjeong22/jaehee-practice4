import streamlit as st

st.set_page_config(page_title="예적금 관리", layout="centered")
st.title("예/적금 관리 (💰)")

st.write("원하는 상품을 선택하고 금액을 입력한 뒤 '만기 금액 조회' 버튼을 누르세요.")

# 상품 선택
product = st.selectbox("상품을 선택하세요", ["예금", "적금 A", "적금 B"], key="saving_product")

# (이미지 안내 블록 제거 - 사용자가 요청한 대로 업로더/URL 코드가 없습니다)

# 금액 입력 (상품별 유효 범위/스텝 적용)
amount = None
if product == "예금":
    amount = st.number_input("저금할 금액을 입력하세요", min_value=1, step=1, format="%d", key="deposit_amount")
elif product == "적금 A":
    amount = st.number_input("저금할 금액을 입력하세요 (20 단위, 20 ~ 180)", min_value=20, max_value=180, step=20, format="%d", key="installment_a_amount")
elif product == "적금 B":
    amount = st.number_input("저금할 금액을 입력하세요 (20 단위, 200 ~ 360)", min_value=200, max_value=360, step=20, format="%d", key="installment_b_amount")

# 만기 금액 조회 버튼
if st.button("만기 금액 조회"):
    # 입력 검증
    try:
        amt = int(amount)
    except Exception:
        st.error("유효한 숫자를 입력하세요.")
    else:
        if amt <= 0:
            st.error("금액은 1 이상의 숫자여야 합니다.")
        else:
            # 이자 계산 (한 달치)
            if product == "예금":
                # 예금: 1% 이자
                interest_rate = 0.01
                interest = amt * interest_rate
                maturity = amt + interest
                st.success(f"원금 {amt} 젤리 + 이자 {interest:.0f} 젤리 → 만기 금액: {maturity:.0f} 젤리")
            elif product == "적금 A":
                # 적금 A: 월 이자율 10%, 원금은 20 단위 20~180
                if amt < 20 or amt > 180 or (amt % 20 != 0):
                    st.error("적금 A의 원금은 20부터 20 단위로 180까지 가능합니다.")
                else:
                    interest_rate = 0.10
                    interest = amt * interest_rate
                    maturity = amt + interest
                    st.success(f"원금 {amt} 젤리 + 이자 {interest:.0f} 젤리 → 만기 금액: {maturity:.0f} 젤리")
            elif product == "적금 B":
                # 적금 B: 월 이자율 20%, 원금은 200부터 20 단위로 360까지
                if amt < 200 or amt > 360 or (amt % 20 != 0):
                    st.error("적금 B의 원금은 200부터 20 단위로 360까지 가능합니다.")
                else:
                    interest_rate = 0.20
                    interest = amt * interest_rate
                    maturity = amt + interest
                    st.success(f"원금 {amt} 젤리 + 이자 {interest:.0f} 젤리 → 만기 금액: {maturity:.0f} 젤리")
