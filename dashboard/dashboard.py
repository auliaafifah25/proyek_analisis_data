import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')



#CREATE DAILY_RENTALS_DF() DIGUNAKAN UNTUK MENYIAPKAN DAILY_RENTALS_DF
def create_daily_rentals_df(df):
    daily_rentals_df= df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    daily_rentals_df.index = daily_rentals_df.index.strftime('%d-%b-%y')
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "dteday": "Periode",
        "cnt": "Jumlah keseluruhan",
        "casual": "Jumlah peminjam biasa",
        "registered": "Jumlah peminjam terdaftar"
    }, inplace=True)
    
    return daily_rentals_df

#CREATE SEASON_RENTALS_DF() DIGUNAKAN UNTUK MENYIAPKAN SEASON_RENTALS_DF
def create_season_rentals_df(df):
    season_rentals_df= df.groupby('season').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': "sum"
    }).reset_index()
    season_rentals_df.rename(columns={
        'season': 'Musim',
        "cnt": "Jumlah keseluruhan",
        "casual": "Jumlah peminjam biasa",
        "registered": "Jumlah peminjam terdaftar"
    }, inplace=True)
    
    return season_rentals_df

#CREATE WEATHERSIT_RENTALS_DF() DIGUNAKAN UNTUK MENYIAPKAN WEATHERSIT_RENTALS_DF
def create_weathersit_rentals_df(df):
    weathersit_rentals_df= df.groupby('weathersit').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': "sum"
    }).reset_index()
    weathersit_rentals_df.rename(columns={
        'weathersit': 'Cuaca',
        "cnt": "Jumlah keseluruhan",
        "casual": "Jumlah peminjam biasa",
        "registered": "Jumlah peminjam terdaftar"
    }, inplace=True)
    
    return weathersit_rentals_df

#CREATE WEEKDAY_RENTALS_DF() DIGUNAKAN UNTUK MENYIAPKAN WEEKDAY_RENTALS_DF
def create_weekday_rentals_df(df):
    weekday_rentals_df= df.groupby('weekday').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': "sum"
    }).reset_index()
    weekday_rentals_df.rename(columns={
        'weekday': 'Perminggu',
        "cnt": "Jumlah keseluruhan",
        "casual": "Jumlah peminjam biasa",
        "registered": "Jumlah peminjam terdaftar"
    }, inplace=True)
    
    return weekday_rentals_df

#CREATE HR_GROUP_RENTALS_DF() DIGUNAKAN UNTUK MENYIAPKAN HR_GROUP_RENTALS_DF
def create_hr_group_rentals_df(df):
    hr_group_rentals_df= df.groupby('hr_group').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': "sum"
    }).reset_index()
    hr_group_rentals_df.rename(columns={
        'hr_group': 'Kelompok waktu',
        "cnt": "Jumlah keseluruhan",
        "casual": "Jumlah peminjam biasa",
        "registered": "Jumlah peminjam terdaftar"
    }, inplace=True)
    
    return hr_group_rentals_df


#LOAD BERKAS MAIN_DATA.CSV SEBAGAI SEBUAH DATAFRAME
all_df = pd.read_csv("https://raw.githubusercontent.com/auliaafifah25/proyek_analisis_data/main/dashboard/main_data.csv")


#MENGURUTKAN DATAFRAME BERDASARKAN DTEDAY SERTA MEMASTIKAN KEDUA KOLOM TERSEBUT BERTIPE DATETIME
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
    
#UNTUK MEMBUAT FILTER DENGAN WIDGET DATE INPUT SERTA MENAMBAHKAN LOGO PERUSAHAAN PADA SIDEBAR
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.gambaranimasi.org/data/media/237/animasi-bergerak-sepeda-0075.gif")
    
    # Mengambil start_date & end_date dari date_input
    start_date = st.date_input(
        label="Rentang Waktu Awal",
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )
    
    end_date = st.date_input(
        label="Rentang Waktu Akhir",
        min_value=start_date,  
        max_value=max_date,
        value=max_date
    )
    
#DATA YANG TELAH DIFILTER SELANJUTNYA AKAN DISIMPAN DALAM MAIN_DF
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]


#UNTUK MENGHASILKAN BERBAGAI DATAFRAME YANG DIBUTUHKAN UNTUK MEMBUAT VISUALISASI DATA
daily_rentals_df= create_daily_rentals_df(main_df)
season_rentals_df= create_season_rentals_df(main_df)
weathersit_rentals_df= create_weathersit_rentals_df(main_df)
weekday_rentals_df= create_weekday_rentals_df(main_df)
hr_group_rentals_df= create_hr_group_rentals_df(main_df)

#MENAMBAHKAN HEADER PADA DASHBOARD 
st.header(':bike: Bike Rentals Collection Dashboard :bike:')

#MEMBUAT PALLETE UNTUK NILAI KHUSUS (YANG TERTINGGI)
def create_palette(data, column):
    max_value = data[column].max()
    palette = [("#72BCD4" if val == max_value else "#D3D3D3") for val in data[column]]
    return palette


#MENAMPILKAN INFORMASI JUMLAH KESELURUHAN, PEMINJAM BIASA, DAN PEMINJAM TERDAFTAR DALAM BENTUK METRIC() YANG DITAMPILKAN MENGGUNAKAN LAYOUT COLUMNS()
#INFORMASI TENTANG JUMLAH RENTAL HARIAN DITAMPILKAN DALAM BENTUK VISUALISASI DATA
st.subheader('Daily Orders')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = daily_rentals_df["Jumlah keseluruhan"].sum()
    st.metric("Jumlah keseluruhan", value=total_rentals)

with col2:
    total_rentals = daily_rentals_df["Jumlah peminjam biasa"].sum()
    st.metric("Peminjam biasa", value=total_rentals)

with col3:
    total_rentals = daily_rentals_df["Jumlah peminjam terdaftar"].sum()
    st.metric("Peminjam terdaftar", value=total_rentals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["Periode"], 
    daily_rentals_df["Jumlah keseluruhan"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=12)  
ax.tick_params(axis='x', labelsize=10)  
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Jumlah Keseluruhan Rental", fontsize=16)

st.pyplot(fig)


#MENYERTAKAN INFORMASI TENTANG JUMLAH RENTAL SEPEDA BERDASARKAN SEASON
#MENAMPILKAN JUMLAH PEMINJAM BERDASARKAN MUSIM DARI TERTINGGI DAN TERENDAH MELALUI SEBUAH VISUALISASI DATA
st.subheader("BERDASARKAN MUSIM")

fig, ax = plt.subplots(figsize=(16, 6))

palette_cnt = create_palette(season_rentals_df, 'Jumlah keseluruhan')
sns.barplot(data=season_rentals_df, x='Musim', y='Jumlah keseluruhan', ax=ax, palette=palette_cnt)
ax.set_title('Jumlah keseluruhan')
ax.set_xlabel(None)
ax.set_ylabel(None)

st.pyplot(fig)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

palette_casual = create_palette(season_rentals_df, 'Jumlah peminjam biasa')
sns.barplot(data=season_rentals_df, x='Musim', y='Jumlah peminjam biasa', ax=ax[0], palette=palette_casual)
ax[0].set_title('Jumlah peminjam biasa')
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

palette_registered = create_palette(season_rentals_df, 'Jumlah peminjam terdaftar')
sns.barplot(data=season_rentals_df, x='Musim', y='Jumlah peminjam terdaftar', ax=ax[1], palette=palette_registered)
ax[1].set_title('Jumlah peminjam terdaftar')
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

st.pyplot(fig)


#MENYERTAKAN INFORMASI TENTANG JUMLAH RENTAL SEPEDA BERDASARKAN WEATHERSIT
#MENAMPILKAN JUMLAH PEMINJAM BERDASARKAN WEATHERSIT DARI TERTINGGI DAN TERENDAH MELALUI SEBUAH VISUALISASI DATA
st.subheader("BERDASARKAN CUACA")

fig, ax = plt.subplots(figsize=(16, 6))

palette_cnt = create_palette(weathersit_rentals_df, 'Jumlah keseluruhan')
sns.barplot(data=weathersit_rentals_df, x='Cuaca', y='Jumlah keseluruhan', ax=ax, palette=palette_cnt)
ax.set_title('Jumlah keseluruhan')
ax.set_xlabel(None)
ax.set_ylabel(None)

st.pyplot(fig)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

palette_casual = create_palette(weathersit_rentals_df, 'Jumlah peminjam biasa')
sns.barplot(data=weathersit_rentals_df, x='Cuaca', y='Jumlah peminjam biasa', ax=ax[0], palette=palette_casual)
ax[0].set_title('Jumlah peminjam biasa')
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

palette_registered = create_palette(weathersit_rentals_df, 'Jumlah peminjam terdaftar')
sns.barplot(data=weathersit_rentals_df, x='Cuaca', y='Jumlah peminjam terdaftar', ax=ax[1], palette=palette_registered)
ax[1].set_title('Jumlah peminjam terdaftar')
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

st.pyplot(fig)


#MENYERTAKAN INFORMASI TENTANG JUMLAH RENTAL SEPEDA BERDASARKAN WEEEKDAY
#MENAMPILKAN JUMLAH PEMINJAM BERDASARKAN WEEKDAY DARI TERTINGGI DAN TERENDAH MELALUI SEBUAH VISUALISASI DATA
st.subheader("BERDASARKAN HARI")

fig, ax = plt.subplots(figsize=(16, 6))

palette_cnt = create_palette(weekday_rentals_df, 'Jumlah keseluruhan')
sns.barplot(data=weekday_rentals_df, x='Perminggu', y='Jumlah keseluruhan', ax=ax, palette=palette_cnt)
ax.set_title('Jumlah keseluruhan')
ax.set_xlabel(None)
ax.set_ylabel(None)

st.pyplot(fig)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

palette_casual = create_palette(weekday_rentals_df, 'Jumlah peminjam biasa')
sns.barplot(data=weekday_rentals_df, x='Perminggu', y='Jumlah peminjam biasa', ax=ax[0], palette=palette_casual)
ax[0].set_title('Jumlah peminjam biasa')
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

palette_registered = create_palette(weekday_rentals_df, 'Jumlah peminjam terdaftar')
sns.barplot(data=weekday_rentals_df, x='Perminggu', y='Jumlah peminjam terdaftar', ax=ax[1], palette=palette_registered)
ax[1].set_title('Jumlah peminjam terdaftar')
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

st.pyplot(fig)


#MENYERTAKAN INFORMASI TENTANG JUMLAH RENTAL SEPEDA BERDASARKAN KELOMPOK WAKTU
#MENAMPILKAN JUMLAH PEMINJAM BERDASARKAN KELOMPOK WAKTU DARI TERTINGGI DAN TERENDAH MELALUI SEBUAH VISUALISASI DATA
st.subheader("BERDASARKAN KELOMPOK WAKTU")

fig, ax = plt.subplots(figsize=(16, 6))

palette_cnt = create_palette(hr_group_rentals_df, 'Jumlah keseluruhan')
sns.barplot(data=hr_group_rentals_df, x='Kelompok waktu', y='Jumlah keseluruhan', ax=ax, palette=palette_cnt)
ax.set_title('Jumlah keseluruhan')
ax.set_xlabel(None)
ax.set_ylabel(None)

st.pyplot(fig)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

palette_casual = create_palette(hr_group_rentals_df, 'Jumlah peminjam biasa')
sns.barplot(data=hr_group_rentals_df, x='Kelompok waktu', y='Jumlah peminjam biasa', ax=ax[0], palette=palette_casual)
ax[0].set_title('Jumlah peminjam biasa')
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

palette_registered = create_palette(hr_group_rentals_df, 'Jumlah peminjam terdaftar')
sns.barplot(data=hr_group_rentals_df, x='Kelompok waktu', y='Jumlah peminjam terdaftar', ax=ax[1], palette=palette_registered)
ax[1].set_title('Jumlah peminjam terdaftar')
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

st.pyplot(fig)

