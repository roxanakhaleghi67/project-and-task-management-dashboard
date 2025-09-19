# داشبورد پروژه — Streamlit

یک دمو ساده برای نمایش EV / PV / AC و رسم S-Curve با Streamlit.

## اجرا لوکال
1. ساخت virtualenv:
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
