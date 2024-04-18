import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Page configuration
st.set_page_config(
    page_title="Kemiskinan Anak-Anak Di Berbagai Negara",
    layout="wide",
    initial_sidebar_state="expanded")

# Membaca dataset
data = pd.read_csv("Data tingkat kemiskinan anak.csv")

# Mengubah nama kolom menjadi lebih deskriptif
data.columns = ['Total', 'Poorest 20%', 'Richest 20%', 'Difference', 'Country Encoded',
                'Country: Albania', 'Country: Algeria', 'Country: Argentina', 'Country: Bangladesh',
                'Country: Belize', 'Country: Bhutan', 'Country: Bosnia and Herzegovina',
                'Country: Costa Rica', 'Country: Dominican Republic', 'Country: El Salvador',
                'Country: Georgia', 'Country: Ghana', 'Country: Guyana', 'Country: Honduras',
                'Country: Jamaica', 'Country: Jordan', 'Country: Kazakhstan', 'Country: Kyrgyzstan',
                'Country: Lao People\'s Democratic Republic', 'Country: Mexico', 'Country: Mongolia',
                'Country: Montenegro', 'Country: Morocco', 'Country: Panama', 'Country: Republic of Moldova',
                'Country: Serbia', 'Country: Suriname', 'Country: Syrian Arab Republic', 'Country: Tajikistan',
                'Country: Thailand', 'Country: The former Yugoslav Republic of Macedonia',
                'Country: Trinidad and Tobago', 'Country: Tunisia', 'Country: Turkmenistan',
                'Country: Uzbekistan', 'Country: Viet Nam', 'Country: Yemen']

# Menghapus kolom yang tidak diperlukan
data = data.drop(columns=['Country Encoded'])

# Sidebar
st.sidebar.title("Dashboard Visualisasi Anak-Anak Di Berbagai Negara")
visualization = st.sidebar.selectbox("Pilih Visualisasi", ("Piramida Penduduk", "Perbandingan Negara"))

# Visualisasi: Piramida Penduduk
if visualization == "Piramida Penduduk":
    st.title("Piramida Penduduk Kemiskinan Anak")
    country = st.selectbox("Pilih Negara", data.columns[5:])
    country_data = data[['Total', 'Poorest 20%', 'Richest 20%']].loc[data[country] == 1]
    country_data = country_data.iloc[0]
    
    # Membuat piramida penduduk menggunakan matplotlib
    fig, ax = plt.subplots()
    
    age_groups = ['Total', 'Poorest 20%', 'Richest 20%']
    values = country_data.values
    
    ax.barh(age_groups, values)
    ax.set_xlabel('Jumlah Anak')
    ax.set_ylabel('Kelompok Kemiskinan')
    ax.set_title(f'Piramida Penduduk Kemiskinan Anak di {country}')
    
    st.pyplot(fig)

# Visualisasi: Perbandingan Negara
elif visualization == "Perbandingan Negara":
    st.title("Perbandingan Tingkat Kemiskinan Anak antar Negara")
    countries = st.multiselect("Pilih Negara", data.columns[5:])
    
    # Melakukan filtering data berdasarkan negara yang dipilih
    selected_data = data[['Total', 'Poorest 20%', 'Richest 20%'] + countries].loc[data[countries].sum(axis=1) > 0]
    
    # Mengubah format data menjadi long format
    selected_data = pd.melt(selected_data, id_vars=['Total', 'Poorest 20%', 'Richest 20%'], value_vars=countries, var_name='Negara', value_name='Kemiskinan Anak')
    
    # Mengubah nama kolom 'variable' menjadi 'Kelompok Kemiskinan'
    selected_data = selected_data.rename(columns={'variable': 'Kelompok Kemiskinan'})
    
    # Membuat visualisasi menggunakan seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Negara', y='Kemiskinan Anak', data=selected_data)
    plt.title("Perbandingan Tingkat Kemiskinan Anak antar Negara")
    plt.xlabel("Negara")
    plt.ylabel("Jumlah Anak")
    plt.xticks(rotation=45)
    plt.legend(title='Kelompok Kemiskinan')

    st.pyplot(plt)