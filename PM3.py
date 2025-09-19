import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="داشبورد پروژه — S-Curve & EV", layout="wide")

st.title("📊 داشبورد پروژه پیشرفته")

st.sidebar.header("🔧 تنظیمات و آپلود فایل")
project_file = st.sidebar.file_uploader("فایل پروژه (CSV / XLSX)", type=["csv","xlsx"], key="proj")
daily_file = st.sidebar.file_uploader("فایل پیشرفت روزانه (برای S-Curve)", type=["csv","xlsx"], key="daily")

@st.cache_data
def read_file(uploaded):
    if uploaded is None:
        return None
    if uploaded.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded)
    else:
        return pd.read_excel(uploaded)

def safe_numeric(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

df = read_file(project_file)
df_daily = read_file(daily_file)

st.markdown("""
### 📂 راهنمای بارگذاری فایل پروژه:
فایل اکسل یا CSV شما باید شامل ستون‌های زیر باشد:
- **Activity** → نام فعالیت یا تسک پروژه  
- **PV** → Planned Value (ارزش برنامه‌ریزی‌شده)  
- **EV** → Earned Value (ارزش کسب‌ شده)  
- **AC** → Actual Cost (هزینه واقعی)  
- **Planned %** → درصد پیشرفت برنامه‌ای  
- **Actual %** → درصد پیشرفت واقعی  
⚠️ نام ستون‌ها دقیقاً همین باشد (حساس به فاصله و حروف).
""")

st.markdown("""
### 📂 راهنمای بارگذاری فایل پیشرفت روزانه:
فایل اکسل یا CSV شما باید شامل ستون‌های زیر باشد:
- **Date** → تاریخ (قابل تبدیل به datetime)  
- **Activity** → نام فعالیت  
- **Planned_EV** → Planned cumulative EV یا مقدار روزانه  
- **Actual_EV** → Actual cumulative EV یا مقدار روزانه  
""")

if df is None:
    st.warning("⚠️ لطفاً ابتدا فایل پروژه را از سایدبار بارگذاری کنید.")
else:
    # پاکسازی و نوع‌دهی
    df.columns = df.columns.str.strip()
    safe_numeric(df, ["PV","EV","AC","Planned %","Actual %"])

    # محاسبه شاخص کل پروژه
    total_PV = df["PV"].sum()
    total_EV = df["EV"].sum()
    total_AC = df["AC"].sum()

    project_SPI = total_EV / total_PV if total_PV != 0 else 0
    project_CPI = total_EV / total_AC if total_AC != 0 else 0
    project_progress = (total_EV / total_PV * 100) if total_PV != 0 else 0
    BAC = total_PV  # Budget at Completion (مجموع برنامه)
    SV = total_EV - total_PV
    CV = total_EV - total_AC
    EAC = total_AC + (BAC - total_EV) / project_CPI if project_CPI != 0 else np.nan
    ETC = EAC - total_AC if EAC is not np.nan else np.nan
    VAC = BAC - EAC if EAC is not np.nan else np.nan
    # 📊 شاخص‌های کل پروژه
    st.subheader("📊 وضعیت کل پروژه")
    col1, col2, col3 = st.columns(3)
    col1.metric("Progress %", f"{round(project_progress,2)}%")
    col2.metric("SPI", round(project_SPI,2),
                delta="ضعیف" if project_SPI < 1 else "خوب",
                delta_color="inverse")
    col3.metric("CPI", round(project_CPI,2),
                delta="پر هزینه" if project_CPI < 1 else "مناسب",
                delta_color="inverse")

    # ================== شاخص‌های انحراف ==================
    st.subheader("📊 شاخص‌های انحراف")
    col4, col5, col6 = st.columns(3)
    col4.metric("SV (Schedule Variance)", round(SV,2),
                delta="تاخیر" if SV < 0 else "زودتر",
                delta_color="inverse")
    col5.metric("CV (Cost Variance)", round(CV,2),
                delta="هزینه بیشتر" if CV < 0 else "هزینه کمتر",
                delta_color="inverse")
    col6.metric("VAC (Variance at Completion)", round(VAC,2) if not np.isnan(VAC) else "N/A",
                delta="کسری بودجه" if VAC < 0 else "بودجه مازاد",
                delta_color="inverse")
    # ---- نمایش داده‌های تسک‌ها
    st.subheader("📋 وضعیت تسک‌ها")
    df["SPI"] = (df["EV"] / df["PV"].replace({0: np.nan})).fillna(0)
    df["CPI"] = (df["EV"] / df["AC"].replace({0: np.nan})).fillna(0)
    st.dataframe(df)

    # ---- نمودار پیشرفت و هزینه تسک‌ها
    selected_activities = st.multiselect("انتخاب فعالیت‌ها", df["Activity"].tolist(), default=df["Activity"].tolist())
    df_filtered = df[df["Activity"].isin(selected_activities)]
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(df_filtered, x="Activity", y=["Planned %", "Actual %"], barmode="group", title="پیشرفت برنامه‌ای و واقعی تسک‌ها")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.line(df_filtered, x="Activity", y=["PV","EV","AC"], markers=True, title="منحنی ارزش کسب شده تسک‌ها")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🔎 CPI و SPI")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=df_filtered["Activity"], y=df_filtered["CPI"], name="CPI"))
    fig3.add_trace(go.Bar(x=df_filtered["Activity"], y=df_filtered["SPI"], name="SPI"))
    fig3.update_layout(barmode="group")
    st.plotly_chart(fig3, use_container_width=True)
    # ================== تحلیل مدیریتی ==================
    st.subheader("📌 تحلیل مدیریتی بر اساس شاخص‌ها")

    col1, col2, col3 = st.columns(3)
    col1.metric("SV (Schedule Variance)", round(SV,2))
    col2.metric("CV (Cost Variance)", round(CV,2))
    col3.metric("VAC (Variance at Completion)", round(VAC,2) if not np.isnan(VAC) else "N/A")

    # ================== پیشنهاد مدیریتی برای همه شاخص‌ها ==================
    st.subheader("📌 پیشنهادهای مدیریتی براساس شاخص‌ها")

    def managerial_advice(SPI, CPI, SV, CV, EAC, BAC, VAC, ETC):
        advices = []

        # SPI
        if SPI < 1:
            advices.append("⏰ پروژه از برنامه زمان‌بندی عقب است. پیشنهاد: افزایش منابع در فعالیت‌های بحرانی.")
        elif SPI > 1:
            advices.append("✅ پروژه جلوتر از برنامه است. پیشنهاد: استفاده از فرصت برای کاهش ریسک یا افزایش دامنه.")
        else:
            advices.append("👌 پروژه مطابق برنامه پیش می‌رود.")

        # CPI
        if CPI < 1:
            advices.append("💸 پروژه بیش‌بود هزینه دارد. پیشنهاد: کنترل هزینه‌های غیرضروری یا بازبینی دامنه.")
        elif CPI > 1:
            advices.append("💰 پروژه صرفه‌جویی در هزینه دارد. پیشنهاد: تخصیص منابع آزاد به فعالیت‌های عقب‌افتاده.")
        else:
            advices.append("👌 هزینه‌ها در سطح برنامه هستند.")

        # SV
        if SV < 0:
            advices.append("⚠️ تأخیر زمانی در برخی فعالیت‌ها وجود دارد. پیشنهاد: بازنگری در برنامه زمان‌بندی.")
        elif SV > 0:
            advices.append("📈 پروژه جلوتر از برنامه است. پیشنهاد: مدیریت ریسک و استفاده از فرصت.")
        
        # CV
        if CV < 0:
            advices.append("⚠️ هزینه‌های واقعی بیشتر از برنامه است. پیشنهاد: کاهش هزینه‌های متغیر.")
        elif CV > 0:
            advices.append("📉 هزینه کمتر از پیش‌بینی است. پیشنهاد: اختصاص بودجه مازاد به مدیریت ریسک.")

        # EAC & VAC
        if EAC > BAC:
            advices.append("❌ پیش‌بینی می‌شود پروژه با بیش‌بود هزینه پایان یابد. پیشنهاد: درخواست بودجه اضافی.")
        elif EAC < BAC:
            advices.append("✅ پیش‌بینی می‌شود پروژه زیر بودجه پایان یابد. پیشنهاد: استفاده از صرفه‌جویی در آینده.")
        
        if VAC < 0:
            advices.append("⚠️ کسری بودجه در پایان پروژه محتمل است. پیشنهاد: بازنگری در منابع و هزینه‌ها.")
        elif VAC > 0:
            advices.append("✅ بودجه اضافه پیش‌بینی می‌شود. پیشنهاد: نگهداشت آن برای ریسک‌های احتمالی.")

        # ETC
        if ETC > (BAC * 0.5):  # مثلا اگر خیلی زیاد باشه
            advices.append("⚠️ هزینه تکمیل باقی‌مانده پروژه بالاست. پیشنهاد: بازبینی محدوده پروژه.")
        else:
            advices.append("👌 هزینه تکمیل پروژه در سطح قابل قبول است.")

        return advices

    advices = managerial_advice(project_SPI, project_CPI, SV, CV, EAC, BAC, VAC, ETC)
    for a in advices:
        st.markdown(f"- {a}")

# S-Curve handling
if df_daily is None and df is not None:
    # ساخت دادهٔ نمونه روزانه (جمع تجمعی) در صورت نبود فایل روزانه
    if not df_daily["Planned_EV"].is_monotonic_increasing:
        try:
            df_daily = pd.DataFrame({
                "Date": pd.date_range("2025-09-01", periods=len(df)),
                "Planned_EV": df["PV"].cumsum().fillna(method="ffill"),
                "Actual_EV": df["EV"].cumsum().fillna(method="ffill")
            })
        except Exception:
            df_daily = None
    else:
        pass

if df_daily is not None:
    df_daily.columns = df_daily.columns.str.strip()
    df_daily["Date"] = pd.to_datetime(df_daily["Date"])
    date_options = sorted(df_daily["Date"].dt.date.unique().tolist())
    start_date, end_date = st.select_slider(
        "بازه زمانی S-Curve",
        options=date_options,
        value=(date_options[0], date_options[-1])
    )
    df_s = df_daily[(df_daily["Date"].dt.date >= start_date) & (df_daily["Date"].dt.date <= end_date)]

    st.subheader("📉 S-Curve پروژه")
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df_s["Date"], y=df_s["Planned_EV"], mode="lines+markers", name="Planned EV"))
    fig4.add_trace(go.Scatter(x=df_s["Date"], y=df_s["Actual_EV"], mode="lines+markers", name="Actual EV"))
    fig4.update_layout(xaxis_title="تاریخ", yaxis_title="ارزش تجمعی")
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("ℹ️ برای نمایش S-Curve، فایل روزانه آپلود کنید یا فایل پروژه بارگذاری شده باشد.")
