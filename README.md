# 🏙️ NYC Airbnb Data Cleaning & Analytics Dashboard

## Overview

This project focuses on cleaning, analyzing, and visualizing the New York City Airbnb Open Data dataset. The dashboard provides interactive insights into Airbnb listings across NYC, helping users explore pricing patterns, neighborhood trends, host statistics, and geographical distribution of properties.

Built using Streamlit, Pandas, and Plotly, the project demonstrates practical data cleaning techniques and interactive business analytics.

---

## Features

### Data Cleaning

* Missing value handling
* Duplicate record removal
* Column standardization
* Price data validation
* Outlier detection and removal using the IQR method

### Interactive Dashboard

* Neighborhood-based filtering
* Price range filtering
* KPI cards for key business metrics
* Interactive NYC Airbnb map
* Price analysis and neighborhood insights
* Download cleaned dataset functionality

### Visualizations

* Airbnb listing locations across NYC
* Average pricing insights
* Neighborhood-wise listing distribution
* Business intelligence metrics

---

## Dataset

**Dataset:** NYC Airbnb Open Data

The dataset contains information about Airbnb listings in New York City, including:

* Listing details
* Host information
* Pricing data
* Geographic coordinates
* Availability metrics
* Review statistics

---

## Tech Stack

* Python
* Pandas
* NumPy
* Streamlit
* Plotly
* PIL
* Git & GitHub

---

## Project Structure

```text
nyc-airbnb-analytics-dashboard/
│
├── data/
│   ├── AB_NYC_2019.csv
│   └── newyork_outline.png
│
├── app.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## Installation

```bash
git clone <repository-url>
cd nyc-airbnb-analytics-dashboard

pip install -r requirements.txt
streamlit run app.py
```

---

## Key Learning Outcomes

* Real-world data cleaning techniques
* Handling missing and inconsistent data
* Outlier detection using statistical methods
* Building interactive dashboards
* Geospatial data visualization
* Business insight generation from raw data

---

## Future Enhancements

* Machine Learning price prediction
* Neighborhood clustering analysis
* Automated insight generation
* Streamlit Cloud deployment
* Advanced geospatial analytics

---

## Author

Nithya Shree

Aspiring Data Analyst | Artificial Intelligence & Data Science Student
