# Household Power Consumption Streamlit Project

## Folder structure

```text
Household_Power_Streamlit/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── household_power_consumption.csv
│
└── pages/
    ├── 1_Introduction.py
    ├── 2_EDA.py
    └── 3_Conclusion.py
```

## Run

Open this folder in VS Code/Terminal:

```bash
pip install -r requirements.txt
```

Then:

```bash
streamlit run app.py
```

The Streamlit sidebar automatically shows Introduction, EDA and Conclusion.

## EDA buttons

The EDA page contains three main buttons:

- Univariate Analysis
- Bivariate Analysis
- Multivariate Analysis

Each section has additional plot buttons.
