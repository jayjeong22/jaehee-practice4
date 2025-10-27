import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="디지털 용돈 기입장", layout="wide")
st.title("디지털 용돈 기입장")

# --- Hero section (simple site-like header with illustration) ---
hero_col1, hero_col2 = st.columns([2, 1])
with hero_col1:
    st.markdown(
        """
        <div style='padding:18px 24px; border-radius:12px; background:linear-gradient(90deg,#f7fbff,#ffffff);'>
            <h1 style='margin:0; font-size:40px; line-height:1.05;'>나의 용돈을 한눈에 — 디지털 용돈 기입장</h1>
            <p style='color:#334155; margin-top:8px; font-size:16px;'>수입·지출·예적금·기부 내역을 간단히 기록하고, 소비 습관에 맞춘 AI 조언을 받아보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
with hero_col2:
    # Decorative illustration (Unsplash). Replace URL if you have a custom image.
    st.image(
        "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=600&q=80",
        use_column_width=True,
    )

    pass

# navigation buttons placed right under the hero sentence
# The buttons set a query param to request the target page and attempt a rerun.
def _safe_rerun():
    try:
        # Prefer the official API when available
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            # fallback: toggle a dummy key and stop to force UI refresh
            st.session_state["_rerun_dummy"] = not st.session_state.get("_rerun_dummy", False)
            st.stop()
    except Exception:
        st.session_state["_rerun_dummy"] = not st.session_state.get("_rerun_dummy", False)
        st.stop()

st.write("")
st.caption("")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("수입 관리"):
        # client-side redirect to set query param so multipage navigates reliably
        components.html("""<script>window.location.search = '?page=a. 수입 관리(➕)';</script>""", height=0)
with nav_col2:
    if st.button("지출 관리"):
        components.html("""<script>window.location.search = '?page=b. 지출 관리(➖)';</script>""", height=0)
with nav_col3:
    if st.button("예적금 관리"):
        components.html("""<script>window.location.search = '?page=c. 예적금 관리(💰)';</script>""", height=0)
with nav_col4:
    if st.button("기부 관리"):
        components.html("""<script>window.location.search = '?page=d. 기부 관리(💌)';</script>""", height=0)

st.markdown("---")

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
    combined.append({"종류": "수입", "설명": f"{month}월 월급", "금액": int(amt)})
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
            st.warning("만 12세의 평균보다 월 지출이 많습니다. 다음 달에는 월급의 일부를 더 저축해보는 것은 어떨까요?")
        else:
            st.success("지출 비율이 안정적입니다. 현재 여유가 있다면 적금 비중을 늘려 미래를 대비해보세요!")

