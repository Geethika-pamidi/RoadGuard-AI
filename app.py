
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RoadGuard AI",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 RoadGuard AI")
st.subheader("Road Accident Intelligence and Analysis System")

@st.cache_data
def load_data():
    return pd.read_csv("RTA Dataset.csv")

try:
    df = load_data()

    st.success("Road accident dataset loaded successfully!")

    # Main statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Accidents", f"{len(df):,}")

    with col2:
        st.metric(
            "Total Casualties",
            f"{df['Number_of_casualties'].sum():,}"
        )

    with col3:
        st.metric(
            "Accident Severity Categories",
            df["Accident_severity"].nunique()
        )

    st.divider()

    # Accident severity analysis
    st.subheader("Accidents by Severity")

    severity_counts = df["Accident_severity"].value_counts()
    st.bar_chart(severity_counts)

    # Weather analysis
    st.subheader("Accidents by Weather Conditions")

    weather_counts = df["Weather_conditions"].value_counts()
    st.bar_chart(weather_counts)

    # Road surface analysis
    st.subheader("Accidents by Road Surface")

    road_counts = df["Road_surface_conditions"].value_counts()
    st.bar_chart(road_counts)

    # Dataset explorer
    st.subheader("Accident Records")
    st.dataframe(df.head(100), use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
