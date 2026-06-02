import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="NYC Airbnb Analytics Dashboard",
    page_icon="🏙️",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/AB_NYC_2019.csv")

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------
def clean_data(df):
    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    # Missing values
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)
    df["name"] = df["name"].fillna("Unknown")
    df["host_name"] = df["host_name"].fillna("Unknown")

    # Remove duplicates
    df = df.drop_duplicates()

    # Ensure numeric price
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])

    # Remove price outliers (IQR)
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    df = df[
        (df["price"] >= lower) &
        (df["price"] <= upper)
    ]

    return df

# ---------------------------------------------------
# DATA
# ---------------------------------------------------
raw_df = load_data()
df = clean_data(raw_df)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
col1, col2 = st.columns([1, 4])

with col1:
    image_path = "data/newyork_outline.png"

    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, width=180)

with col2:
    st.title("🏙️ NYC Airbnb Analytics Dashboard")
    st.markdown(
        """
        Analyze Airbnb listings across New York City.
        Cleaned dataset with interactive filters and business insights.
        """
    )

st.markdown("---")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("Dashboard Filters")

selected_area = st.sidebar.multiselect(
    "Neighbourhood Group",
    options=sorted(df["neighbourhood_group"].unique()),
    default=sorted(df["neighbourhood_group"].unique())
)

price_range = st.sidebar.slider(
    "Price Range (USD)",
    int(df["price"].min()),
    int(df["price"].max()),
    (
        int(df["price"].min()),
        int(df["price"].max())
    )
)

filtered_df = df[
    (df["neighbourhood_group"].isin(selected_area))
    &
    (df["price"] >= price_range[0])
    &
    (df["price"] <= price_range[1])
]

# ---------------------------------------------------
# EMPTY CHECK
# ---------------------------------------------------
if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("📊 Key Metrics")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Listings",
    f"{len(filtered_df):,}"
)

k2.metric(
    "Average Price (USD)",
    f"${filtered_df['price'].mean():.2f}"
)

k3.metric(
    "Maximum Price (USD)",
    f"${filtered_df['price'].max():.2f}"
)

k4.metric(
    "Unique Hosts",
    f"{filtered_df['host_id'].nunique():,}"
)

st.markdown("---")

# ---------------------------------------------------
# BUSINESS INSIGHTS
# ---------------------------------------------------
st.subheader("📈 Business Insights")

st.info(
    f"""
    • Average Airbnb listing price: **${filtered_df['price'].mean():.2f}**

    • Highest listing price: **${filtered_df['price'].max():.2f}**

    • Total listings available: **{len(filtered_df):,}**

    • Unique hosts in selected data: **{filtered_df['host_id'].nunique():,}**
    """
)

# ---------------------------------------------------
# MAP
# ---------------------------------------------------
st.subheader("📍 Airbnb Listings Map")

fig_map = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon="longitude",
    color="price",
    size="minimum_nights",
    hover_name="name",
    hover_data={
        "price": ":$,.2f",
        "minimum_nights": True
    },
    zoom=10,
    height=600
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# ---------------------------------------------------
# PRICE DISTRIBUTION
# ---------------------------------------------------
st.subheader("💰 Price Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="price",
    nbins=50,
    title="Distribution of Airbnb Prices (USD)"
)

fig_hist.update_xaxes(
    title="Price ($)"
)

fig_hist.update_yaxes(
    title="Number of Listings"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ---------------------------------------------------
# TOP NEIGHBOURHOODS
# ---------------------------------------------------
st.subheader("🏘️ Listings by Neighbourhood Group")

area_df = (
    filtered_df["neighbourhood_group"]
    .value_counts()
    .reset_index()
)

area_df.columns = ["Neighbourhood", "Listings"]

fig_bar = px.bar(
    area_df,
    x="Neighbourhood",
    y="Listings",
    color="Neighbourhood",
    text="Listings"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# ---------------------------------------------------
# TOP 10 EXPENSIVE AREAS
# ---------------------------------------------------
st.subheader("💵 Top 10 Most Expensive Areas")

expensive = (
    filtered_df.groupby("neighbourhood_group")["price"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_price = px.bar(
    expensive,
    x="neighbourhood_group",
    y="price",
    color="price",
    text_auto=".2f"
)

fig_price.update_yaxes(
    title="Average Price (USD)"
)

st.plotly_chart(
    fig_price,
    use_container_width=True
)

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------
st.subheader("📄 Cleaned Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Cleaned Dataset",
    data=csv,
    file_name="cleaned_airbnb_data.csv",
    mime="text/csv"
)