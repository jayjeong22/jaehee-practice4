import streamlit as st
import pandas as pd

st.set_page_config(page_title="내 계정 요약", layout="centered")
st.title("디지털 용돈 기입장")

st.write("아래는 내가 학급 화폐를 사용한 기록입니다. '이동' 버튼을 클릭하면 페이지로 이동해 편집할 수 있어요!")

# Ensure session keys exist
incomes = st.session_state.get("incomes", [])
expenses = st.session_state.get("expenses", [])
savings = st.session_state.get("savings", [])
donations = st.session_state.get("donations", [])

### 전체 내역 (한 표로 보기)
st.subheader("전체 거래 내역")
combined = []
# 수입
for inc in incomes:
    # inc expected keys: '월', '수입'
    month = inc.get("월", "")
    amt = inc.get("수입", 0)
    combined.append({"종류": "수입", "설명": f"{month}월", "금액": int(amt)})
# 지출
for exp in expenses:
    month = exp.get("월", "")
    item = exp.get("항목") or f"{month}월"
    amt = exp.get("지출", 0)
    combined.append({"종류": "지출", "설명": item, "금액": int(amt)})
# 예적금
for s in savings:
    prod = s.get("상품") or "예적금"
    amt = s.get("원금") or s.get("만기") or 0
    combined.append({"종류": "예적금", "설명": prod, "금액": int(amt)})
# 기부
for d in donations:
    item = d.get("항목") or "기부"
    amt = d.get("기부(젤리)") or d.get("기부") or 0
    combined.append({"종류": "기부", "설명": item, "금액": int(amt)})

if combined:
    df_combined = pd.DataFrame(combined)
    # 정렬: 종류별로 보여주기
    df_combined = df_combined[["종류", "설명", "금액"]]
    # 인덱스(왼쪽 순서) 없이 마크다운 표로 표시 (st.table이 인덱스를 표시하는 경우 대비)
    md = "| 종류 | 설명 | 금액 |\n|---|---|---:|\n"
    for r in df_combined.to_dict("records"):
        md += f"| {r['종류']} | {r['설명']} | {r['금액']} |\n"
    st.markdown(md)
    # 구분선 추가
    st.markdown("---")
else:
    st.info("아직 기록된 내역이 없습니다. 각 페이지에서 항목을 추가하세요.")


### 더 나은 소비를 위한 AI의 조언 듣기
st.markdown("_사용 내역을 바탕으로 간단한 소비 조언을 받아보세요._")
if st.button("더 나은 소비를 위한 조언 듣기"):
    # 합계 계산
    total_income = 0
    total_expense = 0
    if incomes:
        try:
            total_income = int(pd.DataFrame(incomes)["수입"].sum())
        except Exception:
            total_income = 0
    if expenses:
        try:
            total_expense = int(pd.DataFrame(expenses)["지출"].sum())
        except Exception:
            total_expense = 0

    if total_income == 0:
        if total_expense == 0:
            st.info("수입과 지출 내역이 없습니다. 먼저 각 페이지에서 내역을 추가해 주세요.")
        else:
            st.info("수입 내역이 없습니다. 정확한 조언을 위해 먼저 '수입 관리' 페이지에 수입을 등록해 주세요.")
    else:
        ratio = total_expense / total_income
        # 50% 이상이면 지출 비중이 높음
        if ratio >= 0.5:
            st.warning("당신과 같은 나이 사용자의 평균보다 월 지출이 많습니다. 다음 달에는 월급의 일부를 더 저축해보는 것은 어떨까요?")
        else:
            st.success("지출 비율이 안정적입니다. 현재 여유가 있다면 적금 비중을 늘려 미래를 대비해보세요!")

