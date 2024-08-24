# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="Solar Energy Data Analysis", layout="wide")

# Load the dataset
@st.cache
def load_data():
    data = pd.read_csv('D:/data/processed_data/processed_solar_data.csv')
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data.set_index('Timestamp', inplace=True)
    return data

# Load data
data = load_data()

# Title of the dashboard
st.title("Solar Energy Data Analysis Dashboard")

st.write("""
         This report presents a strategic approach for Moon Light Energy Solutions to enhance 
         operational efficiency and sustainability through targeted solar investments in West Africa. 
         
         By analyzing solar radiation measurement data from Benin, Sierra Leone, and Togo, 
         we aim to identify high-potential regions for solar installation. 
         
         The analysis considers key environmental parameters such as solar irradiance, temperature, 
         humidity, wind speed, and other factors affecting solar energy generation
         """)

# Sidebar for user input
st.sidebar.header("User Input Parameters")

# Select countries for analysis
countries = data['Country'].unique()
selected_countries = st.sidebar.multiselect('Select Countries', countries, default=countries)

# Filter data based on user selection
filtered_data = data[data['Country'].isin(selected_countries)]

# Display basic statistics
st.header("Basic Statistics")
st.write(filtered_data.describe())

# Plotting Solar Irradiance trends
st.header("Solar Irradiance Trends")

fig, ax = plt.subplots(3, 1, figsize=(14, 12))
country_data = filtered_data.groupby('Country')

for i, (country, group) in enumerate(country_data):
    ax[i].plot(group.index, group['GHI'], label='GHI', color='orange')
    ax[i].plot(group.index, group['DNI'], label='DNI', color='blue')
    ax[i].plot(group.index, group['DHI'], label='DHI', color='green')
    ax[i].set_title(f'{country} Solar Irradiance Trends')
    ax[i].set_xlabel('Time')
    ax[i].set_ylabel('Irradiance (W/m²)')
    ax[i].legend()

st.pyplot(fig)

# Analysis of Temperature and Humidity impact on solar efficiency
st.header("Impact of Temperature and Humidity on Solar Efficiency")

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
sns.scatterplot(data=filtered_data, x='Tamb', y='GHI', hue='Country', ax=ax[0])
ax[0].set_title('Ambient Temperature vs GHI')
ax[0].set_xlabel('Ambient Temperature (°C)')
ax[0].set_ylabel('Global Horizontal Irradiance (W/m²)')

sns.scatterplot(data=filtered_data, x='RH', y='GHI', hue='Country', ax=ax[1])
ax[1].set_title('Relative Humidity vs GHI')
ax[1].set_xlabel('Relative Humidity (%)')
ax[1].set_ylabel('Global Horizontal Irradiance (W/m²)')

st.pyplot(fig)

# Wind Speed Analysis
st.header("Wind Speed Distribution by Country")

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(data=filtered_data, x='WS', hue='Country', kde=True, bins=30, ax=ax)
ax.set_title('Wind Speed Distribution by Country')
ax.set_xlabel('Wind Speed (m/s)')
ax.set_ylabel('Frequency')

st.pyplot(fig)

# Analysis of Soiling and Cleaning Impact
st.header("Impact of Cleaning on Solar Panel Performance")

cleaning_effectiveness = filtered_data.groupby(['Country', 'Cleaning'])[['GHI', 'ModA', 'ModB']].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='Country', y='GHI', hue='Cleaning', data=cleaning_effectiveness, ax=ax)
ax.set_title('Impact of Cleaning on GHI')
ax.set_xlabel('Country')
ax.set_ylabel('Average GHI (W/m²)')

st.pyplot(fig)

# Monthly analysis of solar irradiance for seasonality
st.header("Seasonality Analysis: Monthly Average GHI by Country")

filtered_data['Month'] = filtered_data.index.month
monthly_ghi = filtered_data.groupby(['Country', 'Month'])['GHI'].mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(x='Month', y='GHI', hue='Country', data=monthly_ghi, marker='o', ax=ax)
ax.set_title('Monthly Average GHI by Country')
ax.set_xlabel('Month')
ax.set_ylabel('Average GHI (W/m²)')
ax.set_xticks(np.arange(1, 13, 1))

st.pyplot(fig)

# Recommendations based on the analysis
st.header("Recommendations for Solar Investments")

st.write("""
- **Togo and Benin:** High potential regions for solar installations due to high GHI and moderate weather conditions.
- **Sierra Leone:** Suitable for PV installations that can capitalize on diffuse radiation with enhanced maintenance protocols.
- **Technology Selection:** Utilize high-temperature-resistant panels in Togo and Benin to minimize efficiency losses due to heat.
- **Maintenance Strategy:** Develop a predictive maintenance model for cleaning schedules, especially in Sierra Leone, to optimize panel performance.
""")
