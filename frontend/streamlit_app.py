import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append('../backend')

from backend.models.hive_model import Hive
from backend.models.yield_prediction import YieldPrediction
from backend.models.revenue_engine import RevenueEngine
from backend.models.productivity_timeline import ProductivityTimeline
from backend.config import Config

st.set_page_config(page_title="Bee Yield & Profit AI", layout="wide")

st.title("🐝 Bee Yield & Profit AI")
st.markdown("*Predictive Analytics for Bee Colony Profitability*")

# Sidebar - Input Parameters
st.sidebar.header("📋 Hive Configuration")

col1, col2 = st.sidebar.columns(2)
with col1:
    colony_size = st.number_input("Colony Size", min_value=10000, max_value=60000, value=40000, step=1000)
    queen_age = st.number_input("Queen Age (years)", min_value=0.5, max_value=5.0, value=2.5, step=0.5)

with col2:
    hive_strength = st.slider("Hive Strength", 1, 10, 7)
    hive_age_months = st.number_input("Hive Age (months)", min_value=0, max_value=60, value=6)

st.sidebar.markdown("---")
st.sidebar.header("🌍 Environmental Parameters")

col1, col2 = st.sidebar.columns(2)
with col1:
    season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])
    weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Stormy"])

with col2:
    flower_availability = st.selectbox("Flower Availability", ["Low", "Medium", "High"])
    location = st.text_input("Location", "USA")

temperature = st.sidebar.slider("Temperature (°C)", -10, 40, 20)
rainfall = st.sidebar.slider("Rainfall (mm)", 0, 500, 50)

# Create Hive Object
hive = Hive(
    hive_id="HV001",
    colony_size=colony_size,
    queen_age=queen_age,
    hive_strength=hive_strength,
    season=season,
    weather_conditions=weather,
    flower_availability=flower_availability,
    location=location,
    temperature=temperature,
    rainfall=rainfall
)

# Create Prediction Objects
yield_pred = YieldPrediction(hive)
revenue_eng = RevenueEngine(yield_pred, Config.load_market_prices())
timeline = ProductivityTimeline(yield_pred, hive_age_months)

# Main Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🍯 Yield Forecast", "💰 Revenue Analysis", "📅 Timeline"])

with tab1:
    st.subheader("🎯 Hive Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Colony Size", f"{colony_size:,} bees")
    with col2:
        st.metric("Foraging Bees", f"{hive.get_foraging_bees():,}")
    with col3:
        st.metric("Queen Age", f"{queen_age} years")
    with col4:
        st.metric("Efficiency", f"{hive.get_total_efficiency():.1%}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Monthly Honey Yield", f"{yield_pred.predict_monthly_honey():.2f} kg")
        st.metric("Monthly Profit", f"${revenue_eng.calculate_monthly_profit():.2f}")
    with col2:
        st.metric("Yearly Honey Yield", f"{yield_pred.predict_yearly_honey():.2f} kg")
        st.metric("Yearly Profit", f"${revenue_eng.calculate_yearly_profit():.2f}")

with tab2:
    st.subheader("🍯 12-Month Yield Forecast")
    
    forecast_data = yield_pred.forecast_production(12)
    df_forecast = pd.DataFrame(forecast_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_forecast['month'], y=df_forecast['honey_kg'], 
                            mode='lines+markers', name='Honey (kg)', line=dict(color='gold', width=2)))
    fig.add_trace(go.Scatter(x=df_forecast['month'], y=df_forecast['wax_kg'], 
                            mode='lines+markers', name='Beeswax (kg)', line=dict(color='orange', width=2)))
    
    fig.update_layout(title="Monthly Production Forecast", xaxis_title="Month", yaxis_title="Production (kg)",
                     hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df_forecast, use_container_width=True)

with tab3:
    st.subheader("💰 Financial Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Monthly Revenue", f"${revenue_eng.calculate_monthly_revenue():.2f}")
        st.metric("Yearly Revenue", f"${revenue_eng.calculate_yearly_revenue():.2f}")
    with col2:
        st.metric("ROI (%)", f"{revenue_eng.calculate_roi():.1f}%")
        breakeven = revenue_eng.breakeven_months()
        st.metric("Breakeven Period", f"{breakeven} months" if breakeven else "N/A")
    
    revenue_forecast = revenue_eng.forecast_revenue(12)
    df_revenue = pd.DataFrame(revenue_forecast)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_revenue['month'], y=df_revenue['total_revenue'], name='Revenue', marker_color='green'))
    fig.add_trace(go.Bar(x=df_revenue['month'], y=df_revenue['costs'], name='Costs', marker_color='red'))
    fig.add_trace(go.Scatter(x=df_revenue['month'], y=df_revenue['profit'], name='Profit', 
                            mode='lines+markers', line=dict(color='blue', width=2)))
    
    fig.update_layout(title="Monthly Revenue vs Costs vs Profit", barmode='group', 
                     xaxis_title="Month", yaxis_title="USD")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("📅 Productivity Timeline & Lifecycle")
    
    current_phase = timeline.get_current_phase()
    st.info(f"Current Phase: **{current_phase}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Queen Recommendation:**")
        st.write(timeline.get_queen_replacement_recommendation())
    with col2:
        st.write("**Optimal Harvest Period:**")
        harvest_info = timeline.get_optimal_harvest_period()
        st.write(harvest_info['optimal_harvest'])
    
    forecast_5yr = timeline.forecast_5_year_productivity()
    df_5yr = pd.DataFrame(forecast_5yr)
    
    fig = px.line(df_5yr, x='month', y='honey_kg', color='phase', 
                 title="5-Year Productivity Forecast",
                 labels={'month': 'Month', 'honey_kg': 'Honey Production (kg)'})
    st.plotly_chart(fig, use_container_width=True)
    
    lifespan = timeline.estimate_hive_lifespan()
    st.write("**Hive Lifespan Estimate:**")
    st.write(f"Productive Years: {lifespan['productive_years']}")
    st.write(lifespan['recommendation'])

st.markdown("---")
st.markdown("*Made with 🐝 by Bee Yield & Profit AI*")