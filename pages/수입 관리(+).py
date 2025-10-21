import streamlit as st
import pandas as pd

st.set_page_config(page_title="수입 관리", layout="centered")
st.title("수입 관리 (⸝⸝o̴̶̷᷇̂  ̫̣̌ o̴̶̷᷆̂⸝⸝)")

# 세션 상태에 수입 목록 초기화
if "incomes" not in st.session_state:
    st.session_state["incomes"] = []

# 입력 칸: 월(1~12)과 금액(10~250, 10단위) — 텍스트 입력으로 처리하고 검증
col_month, col_amount, col_btn = st.columns([2, 2, 1])
with col_month:
    month_text = st.text_input("몇 월인가요? ", placeholder="예: 3", key="month_input")
with col_amount:
    amount_text = st.text_input("몇 젤리를 받았나요? ", placeholder="예: 50", key="amount_input")
with col_btn:
    apply = st.button("반영하기")

# 입력 검증 및 반영
if apply:
    if not month_text.strip().isdigit():
        st.error("월은 1부터 12 사이의 숫자여야 합니다.")
    elif not amount_text.strip().isdigit():
        st.error("금액은 숫자로 입력하세요 (10단위).")
    else:
        month = int(month_text.strip())
        amount = int(amount_text.strip())
        if not (1 <= month <= 12):
            st.error("월은 1에서 12 사이여야 합니다.")
        elif not (10 <= amount <= 250) or (amount % 10 != 0):
            st.error("금액은 10에서 250 사이이며 10 단위로 입력해야 합니다.")
        else:
            st.session_state["incomes"].append({"월": month, "수입": amount})
            st.success(f"{month}월에 {amount} 젤리 벌었습니다.")

# 등록된 항목을 간단한 표 형태로 표시 (인덱스 제거) 및 각 월별 삭제 버튼 추가
if st.session_state["incomes"]:
    df = pd.DataFrame(st.session_state["incomes"])
    df_group = df.groupby("월", as_index=False)["수입"].sum().sort_values("월")

    st.subheader("수입 내역")
    for _, row in df_group.iterrows():
        m = int(row["월"])
        total = int(row["수입"])
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            st.markdown(f"**{m}월**")
        with c2:
            st.markdown(f"{total} 젤리")
        del_key = f"delete_income_{m}"
        with c3:
            if st.button("삭제", key=del_key):
                # 해당 월의 모든 수입 항목 삭제
                st.session_state["incomes"] = [e for e in st.session_state["incomes"] if int(e.get("월", -1)) != m]
                st.success(f"{m}월의 수입 항목을 삭제했습니다.")
                st.experimental_rerun()

    # 전체 합계 표시
    total_all = int(df_group["수입"].sum())
    st.markdown(f"**합계: {total_all} 젤리**")
else:
    st.info("아직 등록된 수입이 없습니다.")
    