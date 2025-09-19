import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("📊 داشبورد پروژه پیشرفته")
st.markdown("""
### 📂 راهنمای بارگذاری فایل پروژه:
فایل اکسل یا CSV شما باید شامل ستون‌های زیر باشد:

- **Activity** → نام فعالیت یا تسک پروژه  
- **PV** → Planned Value (ارزش برنامه‌ریزی‌شده)  
- **EV** → Earned Value (ارزش کسب‌ شده)  
- **AC** → Actual Cost (هزینه واقعی)  
- **Planned %** → درصد پیشرفت برنامه‌ای  
- **Actual %** → درصد پیشرفت واقعی  

⚠️ دقت کنید که نام ستون‌ها دقیقاً همین باشد (حساس به فاصله و حروف).
""")
st.markdown("""
### 📂 راهنمای بارگذاری فایل پیشرفت روزانه:
فایل اکسل یا CSV شما باید شامل ستون‌های زیر باشد:

- **Date** → نام فعالیت یا تسک پروژه  
- **Activity** → نام فعالیت یا تسک پروژه 
- **Planned_EV** → Planned Value (ارزش برنامه‌ریزی‌ شده)  
- **Actual_EV** → Earned Value (ارزش کسب‌ شده)  

⚠️ دقت کنید که نام ستون‌ها دقیقاً همین باشد (حساس به فاصله و حروف).
""")
# بارگذاری داده
project_file = st.file_uploader("فایل پروژه", type=["xlsx","csv"], key="proj")
daily_file = st.file_uploader("فایل پیشرفت روزانه (برای S-Curve)", type=["xlsx","csv"], key="daily")
df = None
df_daily = None
# =========================
# بخش فایل اصلی پروژه
# =========================
if project_file:
    if project_file.name.endswith(".csv"):
        df = pd.read_csv(project_file)
    else:
        df = pd.read_excel(project_file)
    st.write("📊 داده‌های پروژه:", df.head())
    df.columns = df.columns.str.strip()
    # محاسبه KPI ها
    df["SPI"] = df["EV"] / df["PV"]
    df["CPI"] = df["EV"] / df["AC"]

    st.metric("Overall SPI", round(df["SPI"].mean(), 2))
    st.metric("Overall CPI", round(df["CPI"].mean(), 2))
    # ---- انتخاب بازه فعالیت یا تعداد فعالیت ----
    selected_activities = st.multiselect("فعالیت‌ها را انتخاب کنید", df["Activity"].tolist(), default=df["Activity"].tolist())
    df_filtered = df[df["Activity"].isin(selected_activities)]
        
    # ---- نمودار پیشرفت و هزینه کنار هم ----
    col1, col2 = st.columns(2)
    # نمودار پیشرفت
    with col1:
        fig1 = px.bar(df_filtered, x="Activity", y=["Planned %", "Actual %"], 
                    barmode="group", title="پیشرفت برنامه‌ای و واقعی")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(df_filtered, x="Activity", y=["PV","EV","AC"], markers=True, 
                    title="منحنی ارزش کسب‌ شده")
        st.plotly_chart(fig2, use_container_width=True)

    # ---- نمودار CPI و SPI ----
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=df_filtered["Activity"], y=df_filtered["CPI"], name="CPI"))
    fig3.add_trace(go.Bar(x=df_filtered["Activity"], y=df_filtered["SPI"], name="SPI"))
    fig3.update_layout(barmode="group", title="شاخص عملکرد هزینه و زمان")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("⚠️ لطفاً ابتدا فایل پروژه را بارگذاری کنید.")
    # ---- داده پیش‌فرض S-curve ----
if daily_file:
    if daily_file.name.endswith(".csv"):
        df_daily = pd.read_csv(daily_file)
    else:
        df_daily = pd.read_excel(daily_file)
elif df is not None: 
    # داده نمونه روزانه
    df_daily = pd.DataFrame({
        "Date": pd.date_range("2025-09-01", periods=15),
        "Planned_EV": df["PV"].cumsum(),
        "Actual_EV": df["EV"].cumsum()
    })
if df_daily is not None:
    # ---- اسلایدر بازه زمانی ----
    start_date, end_date = st.select_slider(
        "بازه زمانی S-Curve",
        options=df_daily["Date"],
        value=(df_daily["Date"].min(), df_daily["Date"].max())
    )
    df_s = df_daily[(df_daily["Date"]>=start_date) & (df_daily["Date"]<=end_date)]

    # ---- رسم نمودار S-curve ----
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df_s["Date"], y=df_s["Planned_EV"], mode="lines+markers", name="Planned EV"))
    fig4.add_trace(go.Scatter(x=df_s["Date"], y=df_s["Actual_EV"], mode="lines+markers", name="Actual EV"))
    fig4.update_layout(title="S-Curve پروژه", xaxis_title="تاریخ", yaxis_title="ارزش تجمعی")
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("ℹ️ برای نمایش S-Curve یک فایل روزانه آپلود کنید یا فایل پروژه بارگذاری شود.")