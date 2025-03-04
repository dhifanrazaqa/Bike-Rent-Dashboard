import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_total_rent(df):
    st.metric("Total Rent", value=df["cnt"].sum())
    
def get_total_casual(df):
    st.metric("Total Casual Rent", value=df["casual"].sum())
    
def get_total_registered(df):
    st.metric("Total Registered Rent", value=df["registered"].sum())

def create_best_worst_month(df):
    # Process data
    sum_rent_month_df = df.groupby("mnth", observed=False).cnt.sum().sort_values(ascending=False).reset_index().rename(columns={
        'mnth': 'month',
        'cnt': 'rent_count'
    })
    
    # Create figure
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sum_rent_top_month_df = sum_rent_month_df.head(5)
    print(sum_rent_top_month_df)
    sns.barplot(
        y="month",
        x="rent_count",
        data=sum_rent_top_month_df,
        palette=colors,
        order=sum_rent_top_month_df['month'],
        ax=ax[0]
    )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Bulan dengan peminjam paling banyak", loc="center", fontsize=18)
    ax[0].tick_params(axis='y', labelsize=15)

    sum_rent_worst_month_df = sum_rent_month_df.sort_values(by="rent_count", ascending=True).head(5)
    sns.barplot(
        y="month",
        x="rent_count",
        data=sum_rent_worst_month_df,
        palette=colors,
        order=sum_rent_worst_month_df['month'],
        ax=ax[1]
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Bulan dengan peminjam paling sedikit", loc="center", fontsize=18)
    ax[1].tick_params(axis='y', labelsize=15)

    # Show plot in Streamlit
    st.pyplot(fig)

def create_trend_per_month(df):
    # Process Data
    rent_month_year_df = df.groupby(['yr', 'mnth'], observed=False).agg({
    'instant': 'nunique',
    'cnt': 'sum'
    }).reset_index().rename(columns={
        'yr': 'year',
        'mnth': 'month',
        'instant': 'day_count',
        'cnt': 'rent_count'
    })

    # Create figure
    fig, ax = plt.subplots(figsize=(15, 5))

    # Line plot
    sns.lineplot(
        data=rent_month_year_df,
        x="month",
        y="rent_count",
        hue="year",
        marker="o",
        linewidth=4,
        markersize=12,
        palette=["#72BCD4", "#E50046"],
        ax=ax
    )

    # Title & Labels
    ax.set_title("Rent Count per Month", fontsize=14)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='x', labelsize=14)
    ax.legend(title="Year")

    # Display in Streamlit
    st.pyplot(fig)

def create_best_worst_season(df):
    # Data processing
    sum_rent_season_df = df.groupby("season", observed=False).cnt.sum().sort_values(ascending=False).reset_index().rename(columns={
        'cnt': 'rent_count'
    })

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 4))

    # Define colors
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#72BCD4"]

    # Bar plot
    sns.barplot(
        y="rent_count",
        x="season",
        data=sum_rent_season_df,
        palette=colors,
        ax=ax
    )

    # Title & Labels
    ax.set_title("Best and Worst Performing Season by Number of Rent", loc="center", fontsize=18)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.ticklabel_format(style='plain', axis='y')

    # Display in Streamlit
    st.pyplot(fig)
    
def create_working_day_performance(df):
    # Data processing
    rent_workingday_df = df.groupby('workingday').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False).rename(columns={
        'instant': 'day_count',
        'cnt': 'rent_count'
    }).reset_index()

    # Create figure
    fig, ax = plt.subplots(figsize=(5, 6))

    # Define colors
    colors = ["#72BCD4", "#D3D3D3"]

    # Bar plot
    sns.barplot(
        y="rent_count",
        x="workingday",
        data=rent_workingday_df,
        palette=colors,
        ax=ax
    )

    # Title & Labels
    ax.set_title("Working Day Performance of Bike Rent", loc="center", fontsize=14)
    ax.set_ylabel(None)
    ax.set_xlabel("Is Working Day?", fontsize=20)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=16)
    ax.ticklabel_format(style='plain', axis='y')

    # Display in Streamlit
    st.pyplot(fig)
    
def create_rent_day(df):
    # Data processing
    rent_by_day_df = df.groupby('weekday').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }).rename(columns={
        'instant': 'day_count',
        'cnt': 'rent_count'
    }).reset_index()

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Line plot
    ax.plot(
        rent_by_day_df["weekday"],
        rent_by_day_df["rent_count"],
        marker='o',
        linewidth=6,
        color="#72BCD4",
        markersize=14
    )

    # Title & Labels
    ax.set_title("Number of Rent By Day", loc="center", fontsize=15)
    ax.set_xticks(rent_by_day_df["weekday"])
    ax.tick_params(axis='x', labelsize=18, rotation=30)
    ax.tick_params(axis='y', labelsize=16)

    # Display in Streamlit
    st.pyplot(fig)
    
def create_best_worst_weather(df):
    # Data processing
    rent_weather_df = df.groupby('weathersit').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False).rename(columns={
        'instant': 'day_count',
        'cnt': 'rent_count'
    }).reset_index()

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 4))

    # Colors
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#72BCD4"]

    # Bar plot
    sns.barplot(
        y="rent_count",
        x="weathersit",
        data=rent_weather_df,
        palette=colors,
        ax=ax
    )

    # Title & Labels
    ax.set_title("Best and Worst Performing Weather by Number of Rent", loc="center", fontsize=18)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.ticklabel_format(style='plain', axis='y')

    # Display in Streamlit
    st.pyplot(fig)
    
def create_rent_count_hour(df):
    # Data processing
    rent_workingday_hour_df = df.groupby(['workingday', 'hr']).agg({
        'instant': 'nunique',
        'cnt': 'sum'
    }).reset_index().sort_values(by=['workingday', 'cnt'], ascending=[True, False]).set_index(['workingday', 'hr']).rename(columns={
        'hr': 'hour',
        'instant': 'day_count',
        'cnt': 'rent_count'
    }).reset_index()

    # Create figure
    fig, ax = plt.subplots(figsize=(15, 5))

    # Line plot
    sns.lineplot(
        data=rent_workingday_hour_df,
        x="hr",
        y="rent_count",
        hue="workingday",
        marker="o",
        linewidth=2,
        palette=["#72BCD4", "#E50046"],
        ax=ax
    )

    # Title & Labels
    ax.set_title("Rent Count per Hour (Split by Working Day)", fontsize=15)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xticks(range(0, 24))
    ax.legend(title="Working Day")

    # Display in Streamlit
    st.pyplot(fig)