import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.title("📊 Exploratory Data Analysis")
st.write("Choose an analysis type and then select a plot from the available buttons.")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "household_power_consumption.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, na_values=["?", "NA", "N/A"])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")
    df["Hour"] = df["Time"].dt.hour
    numeric = [
        "Global_active_power", "Global_reactive_power", "Voltage",
        "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"
    ]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Total_Submetering"] = np.sum(
        df[["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]], axis=1
    )
    return df

df = load_data(DATA_PATH)

st.subheader("Choose Analysis")
a, b, c = st.columns(3)
with a:
    uni = st.button("📈 Univariate Analysis", use_container_width=True)
with b:
    bi = st.button("🔗 Bivariate Analysis", use_container_width=True)
with c:
    multi = st.button("🧩 Multivariate Analysis", use_container_width=True)

if "eda_mode" not in st.session_state:
    st.session_state.eda_mode = "univariate"
if uni:
    st.session_state.eda_mode = "univariate"
if bi:
    st.session_state.eda_mode = "bivariate"
if multi:
    st.session_state.eda_mode = "multivariate"

mode = st.session_state.eda_mode
st.divider()

numeric_cols = [
    "Global_active_power", "Global_reactive_power", "Voltage",
    "Global_intensity", "Sub_metering_1", "Sub_metering_2",
    "Sub_metering_3", "Total_Submetering"
]

if mode == "univariate":
    st.header("📈 Univariate Analysis")
    st.caption("Study one variable at a time.")

    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("Histogram", use_container_width=True):
            st.session_state.uni_plot = "hist"
    with p2:
        if st.button("Box Plot", use_container_width=True):
            st.session_state.uni_plot = "box"
    with p3:
        if st.button("Line Trend", use_container_width=True):
            st.session_state.uni_plot = "line"

    if "uni_plot" not in st.session_state:
        st.session_state.uni_plot = "hist"

    col = st.selectbox("Select variable", numeric_cols)
    fig, ax = plt.subplots(figsize=(10, 5))

    if st.session_state.uni_plot == "hist":
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
    elif st.session_state.uni_plot == "box":
        sns.boxplot(x=df[col], ax=ax)
        ax.set_title(f"Box Plot of {col}")
        ax.set_xlabel(col)
    else:
        temp = df[["Date", col]].dropna().head(2000)
        ax.plot(temp["Date"], temp[col])
        ax.set_title(f"{col} over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel(col)
        plt.xticks(rotation=30)

    plt.tight_layout()
    st.pyplot(fig)

elif mode == "bivariate":
    st.header("🔗 Bivariate Analysis")
    st.caption("Study the relationship between two variables.")

    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("Scatter Plot", use_container_width=True):
            st.session_state.bi_plot = "scatter"
    with p2:
        if st.button("Correlation", use_container_width=True):
            st.session_state.bi_plot = "corr"
    with p3:
        if st.button("Power vs Voltage", use_container_width=True):
            st.session_state.bi_plot = "power_voltage"

    if "bi_plot" not in st.session_state:
        st.session_state.bi_plot = "scatter"

    if st.session_state.bi_plot == "scatter":
        x = st.selectbox("X variable", numeric_cols, index=0)
        y = st.selectbox("Y variable", numeric_cols, index=3)
        sample = df[[x, y]].dropna().sample(min(3000, len(df[[x, y]].dropna())), random_state=42)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=sample, x=x, y=y, ax=ax)
        ax.set_title(f"{x} vs {y}")
        st.pyplot(fig)

    elif st.session_state.bi_plot == "corr":
        cols = numeric_cols
        corr = df[cols].corr()
        fig, ax = plt.subplots(figsize=(11, 7))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)

    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(
            data=df.sample(min(3000, len(df)), random_state=42),
            x="Voltage", y="Global_active_power", ax=ax
        )
        ax.set_title("Global Active Power vs Voltage")
        st.pyplot(fig)

elif mode == "multivariate":
    st.header("🧩 Multivariate Analysis")
    st.caption("Study several variables together.")

    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("Correlation Heatmap", use_container_width=True):
            st.session_state.multi_plot = "heatmap"
    with p2:
        if st.button("Sub-metering Comparison", use_container_width=True):
            st.session_state.multi_plot = "submeter"
    with p3:
        if st.button("Hourly Analysis", use_container_width=True):
            st.session_state.multi_plot = "hourly"

    if "multi_plot" not in st.session_state:
        st.session_state.multi_plot = "heatmap"

    if st.session_state.multi_plot == "heatmap":
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(11, 7))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="viridis", ax=ax)
        ax.set_title("Multivariate Correlation Heatmap")
        st.pyplot(fig)

    elif st.session_state.multi_plot == "submeter":
        means = df[["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]].mean()
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(x=means.index, y=means.values, ax=ax)
        ax.set_title("Average Consumption by Sub-metering Category")
        ax.set_ylabel("Average")
        st.pyplot(fig)

    else:
        hourly = df.groupby("Hour")[[
            "Global_active_power", "Global_reactive_power", "Global_intensity"
        ]].mean()
        fig, ax = plt.subplots(figsize=(11, 5))
        hourly.plot(ax=ax)
        ax.set_title("Average Electrical Measurements by Hour")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Average Value")
        st.pyplot(fig)

st.divider()
st.subheader("🔎 Data Summary")
st.dataframe(df[numeric_cols].describe().T, use_container_width=True)
