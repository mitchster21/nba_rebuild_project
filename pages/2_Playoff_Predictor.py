import streamlit as st
import sys
from pathlib import Path
import plotly.express as px
from nba_rebuilds.predictor import PlayoffPredictor

# Load model
@st.cache_resource
def load_model():
    try:
        predictor = PlayoffPredictor()
        return predictor, True
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, False

predictor, model_loaded = load_model()

# Title and description
st.title("🏀 NBA Playoff Return Predictor")
st.markdown("""
This tool predicts how many years it will take for an NBA team to return to the playoffs
after missing the postseason following a playoff appearance.
""")

if not model_loaded:
    st.error("⚠️ Model files not found. Please run the training script first:")
    st.code("python src/nba_rebuilds/train_model.py")
    st.stop()

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Team Roster Information")
    
    roster_size = st.number_input(
        "Roster Size",
        min_value=13,
        max_value=20,
        value=15,
        help="Total number of players on the roster"
    )
    
    retained_players = st.number_input(
        "Retained Players",
        min_value=0,
        max_value=int(roster_size),
        value=8,
        help="Number of players retained from previous season"
    )
    
    new_players = st.number_input(
        "New Players",
        min_value=0,
        max_value=int(roster_size),
        value=7,
        help="Number of new players added"
    )
    
    departed_players = st.number_input(
        "Departed Players",
        min_value=0,
        max_value=20,
        value=7,
        help="Number of players who left from previous season"
    )
    
    continuity_pct = st.slider(
        "Continuity Percentage",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.1,
        help="Percentage of roster retained from previous season"
    )
    
    rookies_count = st.number_input(
        "Number of Rookies",
        min_value=0,
        max_value=10,
        value=2,
        help="Number of rookie players on the roster"
    )
    
    all_nba_count = st.number_input(
        "All-NBA Players",
        min_value=0,
        max_value=5,
        value=0,
        help="Number of All-NBA players on the roster"
    )

with col2:
    st.subheader("Team Age & Experience")
    
    avg_age = st.number_input(
        "Average Age",
        min_value=20.0,
        max_value=35.0,
        value=26.5,
        step=0.1,
        help="Average age of players on the roster"
    )
    
    median_age = st.number_input(
        "Median Age",
        min_value=20.0,
        max_value=35.0,
        value=26.0,
        step=0.1,
        help="Median age of players on the roster"
    )
    
    oldest_player = st.number_input(
        "Oldest Player Age",
        min_value=20,
        max_value=45,
        value=33,
        help="Age of the oldest player"
    )
    
    youngest_player = st.number_input(
        "Youngest Player Age",
        min_value=18,
        max_value=30,
        value=20,
        help="Age of the youngest player"
    )
    
    avg_experience = st.number_input(
        "Average Experience (years)",
        min_value=0.0,
        max_value=20.0,
        value=4.5,
        step=0.1,
        help="Average years of NBA experience"
    )

# Predict button
st.markdown("---")

if st.button("🔮 Predict Playoff Return Time", type="primary", use_container_width=True):
    # Prepare input data
    team_data = {
        'roster_size': roster_size,
        'retained_players': retained_players,
        'new_players': new_players,
        'departed_players': departed_players,
        'continuity_pct': continuity_pct,
        'avg_age': avg_age,
        'median_age': median_age,
        'oldest_player': oldest_player,
        'youngest_player': youngest_player,
        'avg_experience': avg_experience,
        'rookies_count': rookies_count,
        'all_nba_count': all_nba_count
    }
    
    # Predict
    prediction = predictor.predict(team_data)
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Prediction Results")
    
    # Main prediction display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(
            label="Predicted Years to Playoff Return",
            value=f"{prediction:.1f} years",
            help="Expected number of seasons before returning to playoffs"
        )
    
    # Interpretation
    st.markdown("### 💡 Interpretation")
    if prediction < 1.5:
        st.success("🎯 **Quick Recovery Expected** - This team has strong fundamentals for a rapid return to playoff contention.")
    elif prediction < 3:
        st.info("⏳ **Moderate Rebuild** - A typical rebuild timeline. Focus on development and strategic improvements.")
    else:
        st.warning("🔄 **Extended Rebuild** - Significant changes may be needed. Consider long-term strategic planning.")
    
    # Feature importance visualization
    importance_df = predictor.get_feature_importance()
    if importance_df is not None:
        st.markdown("### 📈 Key Factors")
        
        # Create horizontal bar chart
        fig = px.bar(
            importance_df,
            x='importance',
            y='feature',
            orientation='h',
            title='Feature Importance in Prediction',
            color='importance',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Importance Score",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Team profile summary
    st.markdown("### 📋 Team Profile Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Roster Continuity", f"{continuity_pct:.1f}%")
        st.metric("Team Experience", f"{avg_experience:.1f} yrs")
    
    with col2:
        st.metric("Average Age", f"{avg_age:.1f} yrs")
        st.metric("Rookies", f"{rookies_count}")
    
    with col3:
        st.metric("All-NBA Players", f"{all_nba_count}")
        st.metric("Roster Size", f"{roster_size}")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This model predicts playoff return time based on:
    - **Roster composition** (size, turnover, continuity)
    - **Player demographics** (age distribution)
    - **Experience levels** (years in NBA, rookies)
    - **Star power** (All-NBA selections)
    
    The model is trained on NBA data from 2010-11 to 2024-25 seasons.
    """)
    
    st.header("📖 How to Use")
    st.markdown("""
    1. Enter your team's roster characteristics
    2. Click "Predict Playoff Return Time"
    3. Review the prediction and key factors
    4. Use insights for roster planning
    """)
    
    st.header("⚠️ Important Notes")
    st.markdown("""
    - Predictions are based on historical patterns
    - Individual circumstances may vary
    - Consider this as one input in decision-making
    - External factors (injuries, trades, etc.) not included
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>NBA Playoff Return Predictor | Data: 2010-2025 Seasons</div>",
    unsafe_allow_html=True
)