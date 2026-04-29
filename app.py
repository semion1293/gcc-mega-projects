import streamlit as st
import pandas as pd
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Модель ССПЗ", layout="wide")

st.title("Имитационная модель: Влияние мегапроектов на экономику ССПЗ")
st.markdown("Разработано Якименко С. В. для оценки макроэкономического эффекта в рамках дипломного исследования (РАНХиГС).")

# Ввод данных в боковой панели
st.sidebar.header("Параметры моделирования")
investment = st.sidebar.slider("Ежегодные инвестиции (млрд $)", 5, 50, 20)
sector = st.sidebar.selectbox("Основной сектор инвестиций", ["Технологии и ИИ", "Туризм и культура", "Зеленая энергетика", "Логистика"])
institutions = st.sidebar.slider("Индекс институциональной среды (качество законов)", 1.0, 2.5, 1.5)

# Экономическая логика симуляции
years = np.arange(2025, 2046)
base_non_oil_gdp = 80.0 # стартовый несырьевой ВВП

# Коэффициенты зависят от выбранного сектора
if sector == "Технологии и ИИ":
    job_rate = 3000
    sust_index = 80
elif sector == "Туризм и культура":
    job_rate = 8500
    sust_index = 50
elif sector == "Зеленая энергетика":
    job_rate = 4000
    sust_index = 100
else: # Логистика
    job_rate = 5500
    sust_index = 65

# Расчет ВВП по годам
gdp_growth = []
current_gdp = base_non_oil_gdp
for year in years:
    # Мультипликативный эффект от инвестиций и институтов
    growth = (investment * institutions * 0.15) 
    current_gdp += growth
    gdp_growth.append(current_gdp)

df = pd.DataFrame({"Год": years, "Несырьевой ВВП (млрд $)": gdp_growth}).set_index("Год")

# Вывод графиков и метрик
st.subheader("Прогноз роста несырьевого ВВП (2025-2045 гг.)")
st.line_chart(df)

total_jobs = int(investment * 20 * job_rate * (institutions / 1.5))

st.subheader("Макроэкономические итоги за 20 лет")
col1, col2, col3 = st.columns(3)
col1.metric("Создано рабочих мест", f"{total_jobs:,}".replace(',', ' '))
col2.metric("Индекс устойчивости (ESG)", f"{sust_index}/100")
col3.metric("Прирост ВВП к 2045 г.", f"+{int(gdp_growth[-1] - base_non_oil_gdp)} млрд $")
