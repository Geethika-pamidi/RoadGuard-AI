import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import joblib

# 1. Page Configuration
st.set_page_config(page_title="India Air Quality Monitor", layout="wide")
st.title("🌍 Real-Time Air Pollution Monitoring")

# 2. Load your dataset
@st.cache_data
def load_data():
    df = pd.read_csv("air_pollution_data.csv")  # Replace with your actual filename
    return df

try:
    df = load_data()

    # 3. Sidebar for City Selection
    st.sidebar.header("Navigation")
    all_cities = df['city'].unique()
    selected_city = st.sidebar.selectbox("Choose a City", all_cities)

    # 4. Map + Data Table Layout
    city_data = df[df['city'] == selected_city]
    m = folium.Map(
        location=[city_data['latitude'].mean(), city_data['longitude'].mean()],
        zoom_start=10
    )

    # Heatmap layer (only selected city)
    heat_data = city_data[['latitude', 'longitude', 'pollutant_avg']].values.tolist()
    HeatMap(heat_data).add_to(m)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"Pollution Heatmap - {selected_city}")
        st_folium(m, width=900, height=500)
    with col2:
        st.subheader("Recent Pollution Records")
        st.dataframe(city_data.head(10))

    # 5. AQI Prediction (optional model integration)
    st.sidebar.header("AQI Prediction")
    try:
        model = joblib.load("aqi_model.pkl")  # Replace with your model filename
        avg_pollutant = city_data['pollutant_avg'].mean()
        prediction = model.predict([[avg_pollutant]])[0]
        st.sidebar.write("Predicted AQI Category:", prediction)
    except Exception:
        st.sidebar.warning("Prediction model not available. Upload 'aqi_model.pkl' to enable.")

except Exception as e:
    st.error(f"Error loading data: {e}\nPlease ensure 'air_pollution_data.csv' is in the same folder.")
