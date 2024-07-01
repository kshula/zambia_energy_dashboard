import streamlit as st
import pandas as pd
import plotly.express as px
from model_utils import train_ensemble_model, predict_future, preprocess_data


# Set page configuration
st.set_page_config(
    page_title="Zambia Energy Dashboard",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load data
file_path = 'data\lake.csv'

# Preprocess and get the processed lake data
lake = preprocess_data(file_path)

# Train the ensemble model once
scaler, models, meta_model = train_ensemble_model(file_path)

table_1 = pd.read_csv('data\\table_1.csv')

#  Sidebar for navigation
st.sidebar.title("Zambia Energy Dashboard")
page = st.sidebar.radio("Choose a page", ["Home","Large Hydro Power Plants", "Mini-Hydro Power Plants", "Independent Power Producers", "Electricity Imports and Exports", "National Electricity Consumption", "Lake Kariba Water Levels"])

# Large Hydro Power Plants
if page == "Home":    
    # Home page title
    st.title("Welcome to the Zambia Energy Dashboard 🔌")

    # Introduction
    st.write("""
    ### Monitoring and Analyzing Power Supply and Demand in Zambia
    This dashboard provides a comprehensive overview of Zambia's energy sector, focusing on electricity generation, consumption, and the state of Lake Kariba water levels. The aim is to offer insights and data-driven analysis to help understand and address the challenges of power outages and load shedding.
    """)

   
    # Navigation links
    st.markdown("""
    ### Explore the Dashboard
    - **[Power Generation and Consumption](#)**: Analyze electricity generation from various sources, including hydro power plants, mini-hydro plants, and independent power producers.
    - **[Imports and Exports](#)**: Review the trends in electricity imports and exports.
    - **[Sector-wise Consumption](#)**: Understand the electricity consumption patterns across different economic sectors.
    - **[Lake Kariba Water Levels](#)**: Track and predict the water levels of Lake Kariba, crucial for hydro power generation.
    """)

    # Highlight key features
    st.markdown("""
    ### Key Features
    - **Real-time Data Visualization**: Interactive charts and graphs to visualize electricity data.
    - **Predictive Analytics**: Advanced models to predict future water levels and electricity trends.
    - **Comprehensive Insights**: Detailed analysis of power generation, consumption, and the impact of water levels on energy production.
    """)

    # Footer
    st.markdown("""
    ---
    Developed by [Kampamba Shula](#) | [kampambashula@gmail.com](#) | [github/kshula](#)
    """)

elif page == "Large Hydro Power Plants":
    st.title("Electricity Generation from Large Hydro Power Plants (GWh), 2013-2023")
    fig = px.line(table_1, x='Year', y=['Kafue Gorge', 'Kariba North Bank', 'Victoria falls'], title='Electricity Generation from Large Hydro Power Plants Over Time')
    st.plotly_chart(fig)

# Mini-Hydro Power Plants
elif page == "Mini-Hydro Power Plants":
    st.title("Electricity Generation from Mini-Hydro Power Plants (GWh), 2013-2023")
    fig = px.line(table_1, x='Year', y=['Chishimba falls', 'Lunzua', 'Lusiwasi Lower', 'Lusiwasi Upper', 'Musonda Falls', 'Shiwan\'gandu'], title='Electricity Generation from Mini-Hydro Power Plants Over Time')
    st.plotly_chart(fig)

# Independent Power Producers
elif page == "Independent Power Producers":
    st.title("Electricity Generation from Independent Power Producers (GWh), 2013-2023")
    fig = px.line(table_1, x='Year', y=['Bangweulu Power Limited', 'Itezhi tezhi Power Corporation', 'Kafue Gorge Lower', 'Kariba North Bank Extension', 'Lunsemfwa Hydro Power', 'Maamba Collieries Limited', 'Ndola Energy Corporation Limited', 'Ngonye Power Limited'], title='Electricity Generation from Independent Power Producers Over Time')
    st.plotly_chart(fig)

# Electricity Imports and Exports
elif page == "Electricity Imports and Exports":
    st.title("ZESCO's Electricity Imports and Exports (GWh), 2011-2023")
    fig = px.line(table_1, x='Year', y=['Exports', 'Imports'], title='Electricity Imports and Exports Over Time')
    st.plotly_chart(fig)

    fig = px.line(table_1, x='Year', y=['Total_Power', 'Total_Consumption'], title='Electricity Consumption and Production Over Time')
    st.plotly_chart(fig)

# National Electricity Consumption by Economic Sector
elif page == "National Electricity Consumption":
    st.title("Comparison of National Electricity Consumption by Economic Sector (GWh), 2014-2023")
    fig = px.line(table_1, x='Year', y=['Transport', 'Mining (Quarries)', 'Finance and property', 'Trade', 'Manufacturing', 'Domestic (Including households)', 'Agriculture', 'Energy and water', 'Others', 'Construction', 'PPA'], title='National Electricity Consumption by Economic Sector Over Time')
    st.plotly_chart(fig)

# Lake Kariba Water Levels
elif page == "Lake Kariba Water Levels":
    st.title("Lake Kariba Water Levels")
    
    # Plot historical data
    fig = px.line(lake, x='date', y='Target_height_variation', title='Lake Kariba Water Levels Over Time')
    st.plotly_chart(fig)
    
    if st.button(label='Predict Future Water level'):
    
        # Predict future values
        lags = ['lag1', 'lag3', 'lag6']
        steps = 365
        
        # Ensure 'Target_height_variation' is not included in the DataFrame for predictions
        future_predictions = predict_future(lake[['year', 'month', 'day', 'lag1', 'lag3', 'lag6']], lags, steps, scaler, models, meta_model)
        
        # Create a DataFrame for future predictions
        future_dates = pd.date_range(start=lake['date'].max() + pd.Timedelta(days=1), periods=steps)
        future_df = pd.DataFrame({
            'date': future_dates,
            'predicted_Target_height_variation': future_predictions
        })
        
        # Plot future predictions
        fig_future = px.line(future_df, x='date', y='predicted_Target_height_variation', title='Predicted Lake Kariba Water Levels Over Next Year')
        st.plotly_chart(fig_future)