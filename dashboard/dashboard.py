import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile 
import requests
from io import BytesIO

url = 'https://github.com/taufikhidyt/Data-Analysis-Air-Quality-Analysis/raw/main/dashboard/all_df.zip'
response = requests.get(url)
if response.status_code == 200:
    # Membuka file ZIP
    with zipfile.ZipFile(BytesIO(response.content)) as thezip:
        # Membaca file CSV dari dalam file ZIP
        with thezip.open('all_df.csv') as file:
            df = pd.read_csv(file)

df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date


pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
stations = df['station'].unique()

st.title('🌍 Dashboard: Air Quality Analysis')
tab1, tab2, tab3, tab4 = st.tabs(["📈 Fluktuasi Konsentrasi Polutan", 
                                  "📊 Hubungan antar Polutan", 
                                  "🏭 Rata-rata Konsentrasi PM2.5 per Stasiun", 
                                  "🏭 Rata-rata Konsentrasi PM10 per Stasiun"])

with tab1:
    st.header("Fluktuasi Konsentrasi Polutan di Setiap Stasiun")
    st.markdown("Pilih stasiun, polutan, dan rentang waktu untuk melihat perubahan konsentrasi polutan dari waktu ke waktu.")

    selected_station = st.selectbox("Pilih Stasiun", stations)
    selected_pollutant = st.selectbox("Pilih Polutan", pollutants)

    start_date = df['date'].min()
    end_date = df['date'].max()
    selected_date_range = st.slider("Pilih Rentang Tanggal", min_value=start_date, max_value=end_date, value=(start_date, end_date))

    filtered_data = df[(df['station'] == selected_station) & (df['date'].between(selected_date_range[0], selected_date_range[1]))]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='datetime', y=selected_pollutant, data=filtered_data, ax=ax, color="teal", lw=2)

    ax.set_title(f"Fluktuasi {selected_pollutant} di Stasiun {selected_station} ({selected_date_range[0]} hingga {selected_date_range[1]})", fontsize=14, pad=20)
    ax.set_xlabel("Tanggal", fontsize=12)
    ax.set_ylabel(f"Konsentrasi {selected_pollutant}", fontsize=12)
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

with tab2:
    st.header("📊 Hubungan antar Polutan")
    pairplot_fig = sns.pairplot(df[pollutants], kind="scatter", diag_kind="kde", palette="Set1", markers="o")
    st.pyplot(pairplot_fig)

with tab3:
    st.header("🏭 Rata-rata Konsentrasi PM2.5 per Stasiun")
    
    station_pm_avg = df.groupby('station')['PM2.5'].mean().reset_index().sort_values(by='PM2.5', ascending=False)

    fig_pm25, ax_pm25 = plt.subplots(figsize=(12, 8))
    sns.barplot(x='PM2.5', y='station', data=station_pm_avg, palette='viridis')

    for bar in ax_pm25.patches:
        ax_pm25.annotate(f'{bar.get_width():.0f}', 
                         (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                         ha='left', va='center', size=10)

    ax_pm25.set_xlabel('PM2.5 Concentration', labelpad=15)
    ax_pm25.set_ylabel('Station', labelpad=15)
    ax_pm25.set_title("Average PM2.5 Concentration by Station", pad=20)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig_pm25)

with tab4:
    st.header("🏭 Rata-rata Konsentrasi PM10 per Stasiun")
    station_pm_avg1 = df.groupby('station')['PM10'].mean().reset_index().sort_values(by='PM10', ascending=False)

    fig_pm10, ax_pm10 = plt.subplots(figsize=(12, 8))
    sns.barplot(x='PM10', y='station', data=station_pm_avg1, palette='viridis')

    for bar in ax_pm10.patches:
        ax_pm10.annotate(f'{bar.get_width():.0f}', 
                         (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                         ha='left', va='center', size=10)

    ax_pm10.set_xlabel('PM10 Concentration', labelpad=15)
    ax_pm10.set_ylabel('Station', labelpad=15)
    ax_pm10.set_title("Average PM10 Concentration by Station", pad=20)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig_pm10)
