import streamlit as st
import pandas as pd
import plotly.express as px

# Set dark theme
st.set_page_config(page_title="Flipkart Smartphone Analysis", layout="wide")

# Custom CSS for dark theme and bright headers
st.markdown(
    """
    <style>
        body {
            color: #E0E0E0;
            background-color: #121212;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #121212;
            color: #E0E0E0;
        }
        .stTitle {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #00FFF7;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 255, 255, 0.4);
        }
        .section-header {
            font-size: 24px;
            font-weight: bold;
            color: #00FFF7;
            margin-top: 20px;
            text-shadow: 1px 1px 3px rgba(0, 255, 255, 0.5);
            border-bottom: 2px solid #00ADB5;
            padding-bottom: 5px;
        }
        .compare-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .compare-table th, .compare-table td {
            border: 1px solid #00ADB5;
            padding: 8px;
            text-align: center;
            color: #E0E0E0;
        }
        .compare-table th {
            background-color: #00ADB5;
            color: #121212;
            font-weight: bold;
        }
        .compare-table tr:nth-child(even) {
            background-color: #1E1E1E;
        }
        .compare-table tr:nth-child(odd) {
            background-color: #121212;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('flipkart_smartphones.csv')
    data.columns = data.columns.str.lower().str.replace(' ', '_')
    data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
    data['original_price'] = pd.to_numeric(data['original_price'], errors='coerce')
    data['discounted_price'] = pd.to_numeric(data['discounted_price'], errors='coerce')
    data['battery_capacity'] = pd.to_numeric(data['battery_capacity'], errors='coerce')
    data['memory'] = data['memory'].astype(str)
    data['storage'] = data['storage'].astype(str)
    data['rear_camera'] = data['rear_camera'].astype(str)
    data['front_camera'] = data['front_camera'].astype(str)
    data['processor'] = data['processor'].astype(str)
    return data

data = load_data()

# ---- Title ----
st.markdown("<div class='stTitle'>📱 Flipkart Smartphone Data Analysis</div>", unsafe_allow_html=True)

# ---- Brand Market Share ----
st.markdown("<div class='section-header'>🏆 Brand Market Share</div>", unsafe_allow_html=True)
brand_counts = data['brand'].value_counts().reset_index()
brand_counts.columns = ['brand', 'count']

fig_brand_share = px.pie(
    brand_counts,
    names='brand',
    values='count',
    title='Brand Market Share',
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_brand_share.update_layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_brand_share)

# ---- Price vs Ratings ----
st.markdown("<div class='section-header'>💲 Price vs Ratings</div>", unsafe_allow_html=True)

fig_price_vs_rating = px.scatter(
    data,
    x='original_price',
    y='ratings',
    color='brand',
    title='Price vs Ratings',
    hover_data=['model'],
    color_discrete_sequence=px.colors.qualitative.Set1
)

fig_price_vs_rating.update_layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_price_vs_rating)

# ---- Battery vs Price ----
st.markdown("<div class='section-header'>🔋 Battery Capacity vs Price</div>", unsafe_allow_html=True)

fig_battery_vs_price = px.scatter(
    data,
    x='battery_capacity',
    y='original_price',
    color='brand',
    title='Battery Capacity vs Price',
    hover_data=['model'],
    color_discrete_sequence=px.colors.qualitative.Dark24
)

fig_battery_vs_price.update_layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_battery_vs_price)

# ---- Ratings Distribution ----
st.markdown("<div class='section-header'>⭐ Ratings Distribution</div>", unsafe_allow_html=True)

fig_ratings = px.histogram(
    data,
    x='ratings',
    color='brand',
    title='Ratings Distribution',
    nbins=30,
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig_ratings.update_layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    font=dict(color='#E0E0E0'),
    legend=dict(
        font=dict(color='#FFFFFF'),
        bgcolor='#1E1E1E',
        bordercolor='#00ADB5',
        borderwidth=1
    )
)
st.plotly_chart(fig_ratings)

# ---- Compare Smartphones ----
st.markdown("<div class='section-header'>🆚 Compare Smartphones</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    model1 = st.selectbox("Select First Smartphone:", data['model'].unique())

with col2:
    model2 = st.selectbox("Select Second Smartphone:", data['model'].unique())

if model1 and model2:
    phone1 = data[data['model'] == model1].iloc[0]
    phone2 = data[data['model'] == model2].iloc[0]

    st.markdown(f"""
    <table class='compare-table'>
        <tr>
            <th>Feature</th>
            <th>{model1}</th>
            <th>{model2}</th>
        </tr>
        <tr>
            <td>Original Price</td>
            <td>{phone1['original_price']}</td>
            <td>{phone2['original_price']}</td>
        </tr>
        <tr>
            <td>Discounted Price</td>
            <td>{phone1['discounted_price']}</td>
            <td>{phone2['discounted_price']}</td>
        </tr>
        <tr>
            <td>Ratings</td>
            <td>{phone1['ratings']}</td>
            <td>{phone2['ratings']}</td>
        </tr>
        <tr>
            <td>Battery Capacity</td>
            <td>{phone1['battery_capacity']}</td>
            <td>{phone2['battery_capacity']}</td>
        </tr>
        <tr>
            <td>Memory</td>
            <td>{phone1['memory']}</td>
            <td>{phone2['memory']}</td>
        </tr>
        <tr>
            <td>Rear Camera</td>
            <td>{phone1['rear_camera']}</td>
            <td>{phone2['rear_camera']}</td>
        </tr>
        <tr>
            <td>Front Camera</td>
            <td>{phone1['front_camera']}</td>
            <td>{phone2['front_camera']}</td>
        </tr>
        <tr>
            <td>Processor</td>
            <td>{phone1['processor']}</td>
            <td>{phone2['processor']}</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

# ---- Completion Message ----
st.success("✅ Dashboard Loaded Successfully!")
