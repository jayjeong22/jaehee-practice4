import streamlit as st
import pandas as pd

st.set_page_config(page_title="지출 관리", layout="centered")
st.title("지출 관리")

# 세션 상태 초기화
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# 입력 칸: 월(1~12)과 금액(10~250, 10단위) — 텍스트 입력으로 처리하고 검증
col_month, col_amount, col_btn = st.columns([2, 2, 1])
with col_month:
    month_text = st.text_input("몇 월인가요? ", placeholder="예: 3", key="expense_month_input")
with col_amount:
    amount_text = st.text_input("몇 젤리를 지출했나요? ", placeholder="예: 50", key="expense_amount_input")
with col_btn:
    apply = st.button("반영하기")

# 항목은 금액 입력 여부와 상관없이 항상 표시합니다.
selected_item = st.selectbox("항목을 선택하세요", ["권리 구매", "벌금"], key="expense_item")

# 반영 처리
if apply:
    # 기본 검증
    if not month_text.strip().isdigit():
        st.error("월은 1부터 12 사이의 숫자여야 합니다.")
    elif not amount_text.strip().isdigit():
        st.error("금액은 숫자로 입력하세요 (10단위).")
    else:
        month = int(month_text.strip())
        amount = int(amount_text.strip())
        if not (1 <= month <= 12):
            st.error("월은 1에서 12 사이여야 합니다.")
        elif not (10 <= amount <= 1000) or (amount % 10 != 0):
            st.error("금액은 10에서 1000 사이이며 10 단위로 입력해야 합니다.")
        else:
            # 항목 선택 여부 확인
            # 선택박스는 항상 렌더링되므로 session_state 또는 반환값에서 항목을 읽습니다.
            selected_item = st.session_state.get("expense_item", selected_item)
            if not selected_item:
                st.error("항목을 선택하세요.")
            else:
                st.session_state["expenses"].append({"월": month, "항목": selected_item, "지출": amount})
                st.success(f"{month}월에 [{selected_item}] 항목으로 {amount} 젤리 지출이 추가되었습니다.")

# 등록된 지출을 간단한 표 형태로 표시 및 삭제 버튼 추가 (각 월 합계 옆) — 전체 합계 추가
if st.session_state["expenses"]:
    df = pd.DataFrame(st.session_state["expenses"])
    # 월별 합계 계산
    df_group = df.groupby("월", as_index=False)["지출"].sum().sort_values("월")
    st.subheader("지출 내역")
    # 각 행을 직접 렌더링하여 삭제 버튼 추가
    for _, row in df_group.iterrows():
        month = int(row["월"])
        total = int(row["지출"])
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            st.markdown(f"**{month}월**")
        with c2:
            st.markdown(f"{total} 젤리")
        # 고유한 키로 삭제 버튼 생성
        del_key = f"delete_expense_{month}"
        with c3:
            if st.button("삭제", key=del_key):
                # 해당 월의 모든 항목 삭제
                st.session_state["expenses"] = [e for e in st.session_state["expenses"] if int(e.get("월", -1)) != month]
                st.success(f"{month}월의 지출 항목을 삭제했습니다.")
                # Streamlit 버전 차이로 experimental_rerun이 없을 수 있으므로 안전하게 처리
                if hasattr(st, "experimental_rerun") and callable(getattr(st, "experimental_rerun")):
                    try:
                        st.experimental_rerun()
                    except Exception:
                        st.stop()
                else:
                    st.session_state["_rerun_dummy"] = st.session_state.get("_rerun_dummy", 0) + 1
                    st.stop()

    # 전체 합계 표시
    total_all = int(df_group["지출"].sum())
    st.markdown(f"**합계: {total_all} 젤리**")
else:
    st.info("아직 등록된 지출이 없습니다.")
    