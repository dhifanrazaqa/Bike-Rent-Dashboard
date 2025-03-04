import streamlit as st
import pandas as pd
from dashboard_data import *

# Load data
rent_hour_df = pd.read_csv('rent_hour.csv')

# Get date min and date max for filtering
min_date = rent_hour_df["dteday"].min()
max_date = rent_hour_df["dteday"].max()

# Set month and weekday order
rent_hour_df['mnth'] = pd.Categorical(rent_hour_df['mnth'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
rent_hour_df['weekday'] = pd.Categorical(rent_hour_df['weekday'], categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], ordered=True)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.title("Bike Rent 🚲")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
# Filtering Date
main_df = rent_hour_df[(rent_hour_df["dteday"] >= str(start_date)) & 
                (rent_hour_df["dteday"] <= str(end_date))]

# Streamlit UI
st.header("Bike Rent Dashboard 🚲")
get_total_rent(main_df)
colM1, colM2 = st.columns(2)
with colM1:
    get_total_casual(main_df)
with colM2:
    get_total_registered(main_df)
trend_per_month_df = create_trend_per_month(main_df)
    
st.subheader("Peak Hour")
recnt_count_hour = create_rent_count_hour(main_df)
    
st.subheader("Working Day & Weekend Trends")
col3, col4 = st.columns([1, 2])
with col3:
    working_day_performance_df = create_working_day_performance(main_df)
with col4:
    rent_by_day_df = create_rent_day(main_df)

st.subheader("Best and Worst Performing Month by Number of Rent")
best_worst_month_df = create_best_worst_month(main_df)

st.subheader("Best and Worst Performing Weather & Season by Number of Rent")
col1, col2 = st.columns(2)
with col1:
        best_worst_weather_df = create_best_worst_weather(main_df)
with col2:
    best_worst_season_df = create_best_worst_season(main_df)