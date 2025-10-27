import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="디지털 용돈 기입장", layout="wide")

# --- Global CSS & fonts ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    :root{ --primary:#2563eb; --accent:#10b981; --neutral:#64748b; }
    html,body{font-family:'Noto Sans KR', sans-serif;}
    .navbar{position:sticky; top:0; z-index:999; display:flex; align-items:center; justify-content:space-between; padding:10px 18px; background:linear-gradient(90deg,#ffffff,#f8fafc); border-radius:8px; box-shadow:0 2px 10px rgba(2,6,23,0.04);}
    .nav-left{display:flex; align-items:center; gap:12px}
    .logo{width:44px; height:44px; border-radius:8px; background:var(--primary);}
    .nav-menu a{margin:0 10px; color:#0f172a; text-decoration:none; font-weight:700}
    .nav-right{color:#0f172a}

    /* Button / CTA styles (applies to Streamlit native buttons and custom ones) */
    .stButton>button, .btn-primary, .nav-menu a.button-like{background:var(--primary); color:white; padding:10px 16px; border-radius:8px; border:none; font-weight:700;}
    .stButton>button:hover, .btn-primary:hover, .nav-menu a.button-like:hover{opacity:0.95; transform:translateY(-1px)}
    .hero{padding:18px 12px; border-radius:10px; background:linear-gradient(90deg,#f7fbff,#ffffff);}
    .cards{display:flex; gap:16px; margin-top:12px}
    .card{flex:1; padding:14px; border-radius:10px; background:white; box-shadow:0 6px 18px rgba(15,23,42,0.06)}
    .card-title{font-size:13px; color:#475569}
    .card-amount{font-size:20px; font-weight:800; color:var(--primary); margin-top:6px}
    .ai-card{padding:16px; border-radius:10px; background:linear-gradient(90deg,#fffbeb,#fff7ed);}
    footer{margin-top:28px; padding:14px 0; color:#94a3b8; font-size:13px}
        @media (max-width: 720px){ .cards{flex-direction:column} }
        /* Responsive nav: show hamburger on small screens */
        #nav-toggle{display:none}
        .nav-toggle-label{display:none; font-size:20px; padding:6px 10px; border-radius:6px; cursor:pointer}
        @media (max-width:720px){
            .nav-menu{display:none; position:absolute; top:64px; left:10px; right:10px; background:white; flex-direction:column; padding:12px; border-radius:8px; box-shadow:0 8px 24px rgba(2,6,23,0.08)}
            .nav-toggle-label{display:block}
            #nav-toggle:checked ~ .nav-menu{display:flex}
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Navigation bar ---
nav_html = """
<div class='navbar'>
    <div class='nav-left'>
        <div class='logo'></div>
        <div style='font-weight:700'>디지털 용돈 기입장</div>
    </div>
    <input type='checkbox' id='nav-toggle'/>
    <label for='nav-toggle' class='nav-toggle-label'>☰</label>
    <div class='nav-menu'>
        <a class='button-like' href='https://moneypocket.streamlit.app/income'>수입 관리</a>
        <a class='button-like' href='https://moneypocket.streamlit.app/expense'>지출 관리</a>
        <a class='button-like' href='https://moneypocket.streamlit.app/savings'>예적금 관리</a>
        <a class='button-like' href='https://moneypocket.streamlit.app/donation'>기부 관리</a>
    </div>
    <div class='nav-right'>학생님</div>
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)

# --- Hero ---
st.markdown("""
<div class='hero'>
  <h1 style='margin:0; font-size:28px;'>나의 용돈을 한눈에</h1>
  <p style='color:#334155; margin:6px 0 0;'>수입·지출·예적금·기부 내역을 간단히 기록하고, 소비 습관에 맞춘 AI 조언을 받아보세요.</p>
</div>
""", unsafe_allow_html=True)

# small spacing
st.write("")

# --- Summary cards (read session_state and render styled cards) ---
# compute totals safely
total_income = 0
total_expense = 0
total_savings = 0
total_donations = 0
if st.session_state.get("incomes"):
    try:
        total_income = int(pd.DataFrame(st.session_state.get("incomes"))["수입"].sum())
    except Exception:
        total_income = 0
if st.session_state.get("expenses"):
    try:
        total_expense = int(pd.DataFrame(st.session_state.get("expenses"))["지출"].sum())
    except Exception:
        total_expense = 0
if st.session_state.get("savings"):
    try:
        df_s = pd.DataFrame(st.session_state.get("savings"))
        if "만기" in df_s.columns:
            total_savings = int(df_s["만기"].fillna(0).sum())
        else:
            total_savings = int(df_s.get("원금", pd.Series(dtype=int)).fillna(0).sum())
    except Exception:
        total_savings = 0
if st.session_state.get("donations"):
    try:
        df_d = pd.DataFrame(st.session_state.get("donations"))
        # try common donation keys
        amt_col = None
        for c in ["기부(젤리)", "기부"]:
            if c in df_d.columns:
                amt_col = c
                break
        if amt_col:
            total_donations = int(df_d[amt_col].fillna(0).sum())
    except Exception:
        total_donations = 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='card'><div class='card-title'>수입</div><div class='card-amount'>{total_income:,} 젤리</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='card'><div class='card-title'>지출</div><div class='card-amount'>{total_expense:,} 젤리</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='card'><div class='card-title'>예적금</div><div class='card-amount'>{total_savings:,} 젤리</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='card'><div class='card-title'>기부</div><div class='card-amount'>{total_donations:,} 젤리</div></div>", unsafe_allow_html=True)

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
        amt_display = f"{int(r['금액']):,} 젤리"
        md += f"| {r['종류']} | {r['설명']} | {amt_display} |\n"
    st.markdown(md)
    # 구분선 추가
    st.markdown("---")
else:
    st.info("아직 기록된 내역이 없습니다. 각 페이지에서 항목을 추가하세요.")


### 더 나은 소비를 위한 AI의 조언 듣기
st.markdown("<div class='ai-card'><strong>사용 내역을 바탕으로 간단한 소비 조언을 받아보세요!</strong>", unsafe_allow_html=True)
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
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<footer>
    © 2025 젤리공화국 • 교육용 샘플 앱. 이 앱은 학습 목적으로 제공됩니다.
</footer>
""", unsafe_allow_html=True)

