import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_season_frequent_df(df):
    result = df.groupby(by="season").cnt.sum().reset_index()

    season_mapping = {
        1: "Springer",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }

    result['season'] = result['season'].map(season_mapping)
    return result

def create_registered_casual_frequent(df):
    filtered_df = day_df[day_df['yr'] == 1]
    monthly_totals = filtered_df.groupby(by=["mnth"]).agg({
    'registered': 'sum',
    'casual': 'sum'
    }).reset_index()
    return monthly_totals

day_df = pd.read_csv("dashboard/all_data.csv")

# Streamlit App
def main():
    st.title('Bike Sharing Dataset')

    # Display the filtered dataset
    st.subheader('Dataset')
    st.dataframe(day_df)

    # Descriptive statistics
    #st.subheader('Grafik Penyewaan/musim')
    season_frequent_df = create_season_frequent_df(day_df)
    #st.dataframe(season_frequent_df)

    # Histogram Penyewaan Sepeda tiap Musim
    st.subheader('Histogram Penyewaan Sepeda tiap Musim')
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(y="cnt", x="season", data=season_frequent_df.sort_values(by="season", ascending=False), ax=ax)

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
                    textcoords='offset points')

    plt.title("Jumlah Penyewaan Sepeda tiap musim", loc="center", fontsize=15)
    plt.ylabel("Count")
    plt.xlabel("Season")
    plt.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)

    # Scatter plot
    st.subheader('Grafik Penyewa Sepeda')
    monthly_totals = create_registered_casual_frequent(day_df)  # <-- Memanggil fungsi untuk mendapatkan data
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.plot(monthly_totals['mnth'], monthly_totals['casual'], label='Casual', marker='o')
    plt.plot(monthly_totals['mnth'], monthly_totals['registered'], label='Registered', marker='o')
    plt.title("Frekuensi Penyewa Terdaftar dan Biasa Tahun 2012", fontsize=15)
    plt.xlabel("Month")
    plt.ylabel("Frequency")
    plt.legend()
    st.pyplot(fig)


if __name__ == '__main__':
    main()







