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
    amount_text = st.text_input("기부 금액을 입력하세요", placeholder="예: 50", key="donation_amount_input")

# 금액 유효성 확인은 반영 버튼 클릭 시 처리합니다.
# 기부 항목은 금액 입력 여부와 상관없이 항상 표시합니다.
selected_item = st.selectbox("기부 대상을 선택하세요", ["선생님", "친구"], key="donation_item")
apply = st.button("반영하기")

# 반영 처리: 버튼 클릭 시 금액을 검증하고 세션에 저장합니다.
if apply:
    amt_text = amount_text.strip()
    if amt_text == "":
        st.error("기부 금액을 입력하세요. 최소 10젤리 이상입니다.")
    else:
        try:
            amount = int(amt_text)
            if amount < 10:
                st.error("기부할 수 있는 최소 금액은 10젤리입니다.")
            else:
                st.session_state["donations"].append({"항목": selected_item, "기부(젤리)": amount})
                # 성공 직후에는 표를 숨기도록 플래그 설정
                st.session_state["_hide_donation_table"] = True
                st.success(f"{amount}젤리가 기부되었습니다! 당신 덕분에 세상이 더욱 따뜻해졌어요! :)")
        except ValueError:
            st.error("유효한 숫자를 입력해주세요.")

# 등록된 기부 내역 간단한 표로 표시 (인덱스 제거)
# 단, 방금 반영해서 성공 메시지를 보여주는 경우에는 표를 숨깁니다.
if st.session_state["donations"] and not st.session_state.get("_hide_donation_table", False):
    df = pd.DataFrame(st.session_state["donations"])
    st.subheader("기부 내역")
    st.table(df.to_dict("records"))
    