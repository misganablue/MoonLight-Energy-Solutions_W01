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
    df = pd.read_csv('C:/Users/lenovo/Downloads/data/processed_data/processed_solar_data.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    return df
@st.cache
def get_database_connection():
    # Create and return a database connection
    conn = ...
    return conn
# Load data
df = load_data()

# Title of the dashboard
st.title("Solar Energy Data Analysis Dashboard")

# Sidebar for user input
st.sidebar.header("User Input Parameters")

# Select countries for analysis
countries = df['Country'].unique()
selected_countries = st.sidebar.multiselect('Select Countries', countries, default=countries)

# Filter data based on user selection
filtered_data = df[df['Country'].isin(selected_countries)]

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


# Recommendations based on the analysis
st.header("Recommendations for Solar Investments")

st.write("""
- **Togo and Benin:** High potential regions for solar installations due to high GHI and moderate weather conditions.
- **Sierra Leone:** Suitable for PV installations that can capitalize on diffuse radiation with enhanced maintenance protocols.
- **Technology Selection:** Utilize high-temperature-resistant panels in Togo and Benin to minimize efficiency losses due to heat.
- **Maintenance Strategy:** Develop a predictive maintenance model for cleaning schedules, especially in Sierra Leone, to optimize panel performance.
""")
