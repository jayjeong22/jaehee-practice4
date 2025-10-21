import streamlit as st
import pandas as pd

st.set_page_config(page_title="기부 관리", layout="centered")
st.title("기부 관리")

# 세션 상태 초기화
if "donations" not in st.session_state:
    st.session_state["donations"] = []

# 금액 입력 (최소 10, 상한선 없음) — 텍스트 입력으로 받고 검증
col_amt, col_btn = st.columns([2, 1])
with col_amt:
    amount_text = st.text_input("기부 금액을 입력하세요 (최소 10)", placeholder="예: 50", key="donation_amount_input")

# 금액 유효성 확인 (숫자, >=10)
valid_amount = False
if amount_text.strip().isdigit():
    try:
        amt = int(amount_text.strip())
        if amt >= 10:
            valid_amount = True
    except Exception:
        valid_amount = False

# 금액이 유효하면 항목 선택을 보여주고, 선택 완료 시 반영 버튼 표시
selected_item = None
if valid_amount:
    selected_item = st.selectbox("기부 대상을 선택하세요", ["선생님", "친구"], key="donation_item")
    apply = st.button("반영하기")
else:
    st.info("기부 금액은 숫자로 입력하고 최소 10 이상이어야 항목을 선택할 수 있습니다.")

# 반영 처리: 세션에 저장하고 기부증서 표시
if valid_amount and selected_item and 'apply' in locals() and apply:
    amount = int(amount_text.strip())
    st.session_state["donations"].append({"항목": selected_item, "기부(젤리)": amount})
    # 기부증서 출력 (사용자 요청한 문구)
    st.success(f"{amount}원이 기부되었습니다! 당신 덕분에 세상이 더욱 따뜻해졌어요. :)")

# 등록된 기부 내역 간단한 표로 표시 (인덱스 제거)
if st.session_state["donations"]:
    df = pd.DataFrame(st.session_state["donations"])
    st.subheader("기부 내역")
    st.table(df.to_dict("records"))
    