import streamlit as st
import pandas as pd

st.title("🏠 Introduction")
st.markdown("## Household Power Consumption Analysis")
st.write(
    "This project analyzes household electricity consumption using Python, "
    "Pandas, NumPy, Matplotlib and Streamlit."
)

st.subheader("🎯 Project Objectives")
st.markdown("""
- Understand the structure and quality of the electricity dataset.
- Study the distribution of important power-consumption variables.
- Explore relationships between power, voltage, intensity and sub-metering.
- Analyze how electricity usage changes over time.
- Present findings through an easy-to-use interactive dashboard.
""")

st.subheader("📂 Dataset Information")
st.write(
    "The dataset contains timestamped household electricity measurements. "
    "Each record contains date/time information and several electrical measurements."
)

st.subheader("🔎 Main Features")
features = {
    "Date": "Date of measurement",
    "Time": "Time of measurement",
    "Global_active_power": "Global active power consumption",
    "Global_reactive_power": "Global reactive power",
    "Voltage": "Electrical voltage",
    "Global_intensity": "Global intensity",
    "Sub_metering_1": "First sub-metering measurement",
    "Sub_metering_2": "Second sub-metering measurement",
    "Sub_metering_3": "Third sub-metering measurement",
}
st.table(pd.DataFrame(features.items(), columns=["Feature", "Description"]))

st.subheader("🛠️ Technologies Used")
st.success("Streamlit  •  Pandas  •  NumPy  •  Matplotlib  •  Seaborn")
