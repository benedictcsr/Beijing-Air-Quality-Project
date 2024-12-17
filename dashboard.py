import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()


def create_daily_pollution(df):
    period = pd.Grouper(key="datetime", freq="D")
    daily = df.groupby([period, "station"])[["PM2.5"]].mean().reset_index()
    return daily

def create_monthly_pollution(df):
    period = pd.Grouper(key="datetime", freq="M")
    monthly = df.groupby([period, "station"])[["PM2.5"]].mean().reset_index()
    return monthly

def create_hourly_pollution(data):
    hourly = data[(data["datetime"].dt.year==2014) & (data["datetime"].dt.month==2)]
    hourly = hourly.groupby([data["datetime"].dt.hour, "station"])[["PM2.5"]].mean().reset_index()
    return hourly

def create_yearly_pollution():
    highest_pm25_yearly = data.groupby(["year", "station"])[["PM2.5"]].mean().sort_values(["year", "PM2.5"], ascending=[True, False]).reset_index()
    return highest_pm25_yearly

data = pd.read_csv("all_data.csv")
data["datetime"] = pd.to_datetime(data["datetime"])
# period = pd.Grouper(key="datetime", freq="ME")

PM25_data = data.resample("D", on="datetime")[["PM2.5"]].mean().reset_index()

min_date = PM25_data["datetime"].min()
max_date = PM25_data["datetime"].max()

with st.sidebar:
    st.subheader("Air Monitoring Corp")
    start_date, end_date = st.date_input(
        label="Pick a date",
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date])


# Data dari tanggal yang di UI
main_df = data[(data["datetime"] >= str(start_date)) & (data["datetime"] <= str(end_date))]


daily_pollution = create_daily_pollution(main_df)
monthly_pollution = create_monthly_pollution(main_df)
hourly_pollution = create_hourly_pollution(data)
yearly_pollution = create_yearly_pollution()


st.header("Dashboard Polusi PM 2.5")

tab1, tab2 = st.tabs(["Pollution Monitor", "Yearly Report"])

with tab1:
    col1, col2 = st.columns([1,1])
    
    with col1:
        current = PM25_data[PM25_data["datetime"] == str(end_date)]["PM2.5"]
        st.metric("Current PM 2.5 Pollution", value=round(current, 2))
    
    with col2:
        option = st.selectbox(
        "Filter By",
        ("Hari", "Bulan")
    )
    
    if option == "Hari":
        fig, ax = plt.subplots(figsize=(30,15))
        
        sns.lineplot(data=daily_pollution, x=daily_pollution["datetime"].astype(str), y="PM2.5", hue="station", markers=True, style="station", markersize=12)
        ax.set_title("Pergerakan Polusi PM2.5 Perhari di Beijing (Detail)", fontsize=40)
        ax.annotate(f"Highest Point:  {round(daily_pollution["PM2.5"].max(), 2)}", xy=(7, daily_pollution["PM2.5"].max()+2), fontsize=25)
        ax.axhline(y=daily_pollution["PM2.5"].max(), linestyle="--")
        ax.tick_params(axis="x", labelsize=20, labelrotation=45)
        ax.tick_params(axis="y", labelsize=30)
        ax.set_ylim(top=300)
        ax.legend(bbox_to_anchor=(0.275, 0.5, 0.5, 0.5), ncols=5, fontsize=18)
        
        st.pyplot(fig)
        
    elif option == "Bulan":
        fig, ax = plt.subplots(figsize=(30,15))
        
        sns.lineplot(data=monthly_pollution, x=monthly_pollution["datetime"].astype(str), y="PM2.5", hue="station", markers=True, style="station", markersize=12, linewidth=3)
        ax.set_title("Pergerakan Polusi PM2.5 Perbulan di Beijing (Detail)", fontsize=40)
        ax.annotate(f"Highest Point:  {round(monthly_pollution["PM2.5"].max(), 2)}", xy=(2, monthly_pollution["PM2.5"].max()+2), fontsize=25)
        ax.axhline(y=monthly_pollution["PM2.5"].max(), linestyle="--")
        ax.tick_params(axis="x", labelsize=20, labelrotation=45)
        ax.tick_params(axis="y", labelsize=30)
        ax.set_ylim(top=160)
        ax.legend(bbox_to_anchor=(0.28, 0.5, 0.5, 0.5), ncols=5, fontsize=18)
        
        st.pyplot(fig)

    st.divider()
    st.subheader("PM 2.5 Pollution Pattern Within 24 Hours in February 2014")
    
    fig, ax = plt.subplots(figsize=(30,15))
    sns.lineplot(data=hourly_pollution, x="datetime", y="PM2.5", hue="station", markers=True, style="station", markersize=12, linewidth=2)
    ax.legend(bbox_to_anchor=(0.25, 0.5, 0.5, 0.5), ncols=4, fontsize=18)
    ax.tick_params(axis="x", labelsize=25)
    ax.tick_params(axis="y", labelsize=30)
    ax.set_xticks([i for i in range(24)])
    ax.set_xlabel("Hour")

    st.pyplot(fig)
    

    
with tab2:
    st.subheader(f"Yearly PM 2.5 Pollution Report")

    year = data["year"].unique().tolist()
    option_year = st.selectbox(
        "Pick a Year",
        (year)
    )
    
    fig, ax = plt.subplots(figsize=(20,14))
    palette = ["#a6cee3" for i in range(11)]
    palette.insert(0, "#e31a1c")
    
    sns.barplot(yearly_pollution[yearly_pollution["year"]==option_year], x="PM2.5", y="station", hue="station", palette=palette)
    ax.tick_params(axis="x", labelsize=25)
    ax.tick_params(axis="y", labelsize=35)
    ax.set_ylabel("")
    ax.set_xlim(right=yearly_pollution[yearly_pollution["year"]==option_year]["PM2.5"].max()+5)
    for i in range(12):
        ax.bar_label(ax.containers[i], fontsize=20, fmt="%.2f", padding=2)

    st.pyplot(fig)