import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.title("✅ Conclusion")
st.write("This page summarizes the observations generated from the household power dataset.")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "household_power_consumption.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, na_values=["?", "NA", "N/A"])
    for col in [
        "Global_active_power", "Global_reactive_power", "Voltage",
        "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Total_Submetering"] = np.sum(
        df[["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]], axis=1
    )
    return df

df = load_data(DATA_PATH)

means = df[["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]].mean()
highest_sub = means.idxmax()

st.subheader("📌 Key Findings")
st.markdown(f"""
- The dataset contains **{len(df):,} records**.
- The dataset contains **{len(df.columns):,} columns** before derived analysis fields.
- The average Global Active Power is **{df['Global_active_power'].mean():.3f}**.
- The average Voltage is **{df['Voltage'].mean():.2f}**.
- Among the three sub-metering categories, **{highest_sub}** has the highest average value in this dataset.
- The dashboard allows the user to investigate distributions, relationships and combined variable patterns interactively.
""")

st.subheader("💡 Interpretation")
st.info(
    "EDA helps identify patterns, unusual observations and relationships in the electricity data. "
    "The conclusions should be interpreted together with the selected time period and variables."
)

st.subheader("🚀 Future Scope")
st.markdown("""
- Build a machine-learning model for power-consumption prediction.
- Add date-range and hour-range filters.
- Add downloadable reports.
- Deploy the application online using Streamlit Community Cloud.
""")
