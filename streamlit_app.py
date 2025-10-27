import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="내 계정 요약", layout="centered")
st.title("디지털 용돈 기입장")

st.write("아래는 내가 학급 화폐를 사용한 기록입니다. '이동' 버튼을 클릭하면 페이지로 이동해 편집할 수 있어요!")

# Ensure session keys exist
incomes = st.session_state.get("incomes", [])
expenses = st.session_state.get("expenses", [])
savings = st.session_state.get("savings", [])
donations = st.session_state.get("donations", [])

### 나의 수입
st.subheader("나의 수입")
if incomes:
    df_inc = pd.DataFrame(incomes)
    df_group = df_inc.groupby("월", as_index=False)["수입"].sum().sort_values("월")
    labels = df_group["월"].astype(str) + "월"
    sizes = df_group["수입"]
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
    st.markdown(f"**총 수입: {int(df_group['수입'].sum())} 젤리**")
else:
    st.info("아직 등록된 수입이 없습니다. '수입 관리' 페이지에서 항목을 추가하세요.")

### 나의 지출
st.subheader("나의 지출")
if expenses:
    df_exp = pd.DataFrame(expenses)
    # 항목별 분포가 있으면 항목별 파이차트, 없으면 월별
    if "항목" in df_exp.columns:
        df_group = df_exp.groupby("항목", as_index=False)["지출"].sum().sort_values("지출", ascending=False)
        labels = df_group["항목"]
        sizes = df_group["지출"]
    else:
        df_group = df_exp.groupby("월", as_index=False)["지출"].sum().sort_values("월")
        labels = df_group["월"].astype(str) + "월"
        sizes = df_group["지출"]
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
    st.markdown(f"**총 지출: {int(df_group['지출'].sum())} 젤리**")
else:
    st.info("아직 등록된 지출이 없습니다. '지출 관리' 페이지에서 항목을 추가하세요.")

### 나의 예적금
st.subheader("나의 예적금")
if savings:
    df_save = pd.DataFrame(savings)
    if "상품" in df_save.columns and "원금" in df_save.columns:
        df_group = df_save.groupby("상품", as_index=False)["원금"].sum()
        labels = df_group["상품"]
        sizes = df_group["원금"]
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
        st.markdown(f"**총 원금: {int(df_save['원금'].sum())} 젤리 / 총 예상 이자: {int(df_save['이자'].sum())} 젤리**")
    else:
        st.info("예적금 데이터가 충분하지 않아 원그래프로 표시할 수 없습니다.")
else:
    st.info("아직 등록된 예적금 내역이 없습니다. '예적금 관리' 페이지에서 조회해 추가하세요.")

### 나의 기부내역
st.subheader("나의 기부내역")
if donations:
    df_don = pd.DataFrame(donations)
    if "항목" in df_don.columns and "기부(젤리)" in df_don.columns:
        df_group = df_don.groupby("항목", as_index=False)["기부(젤리)"].sum()
        labels = df_group["항목"]
        sizes = df_group["기부(젤리)"]
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
        total_don = int(df_group["기부(젤리)"].sum())
        st.markdown(f"**총 기부액: {total_don} 젤리**")
    else:
        st.info("기부 데이터가 충분하지 않아 원그래프로 표시할 수 없습니다.")
else:
    st.info("아직 등록된 기부 내역이 없습니다. '기부 관리' 페이지에서 추가하세요.")


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

