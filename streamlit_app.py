"""Streamlit app for NBA rebuild analysis."""

from __future__ import annotations
import io
from contextlib import redirect_stdout
import pandas as pd
import streamlit as st

from nba_rebuilds import fetch_data, rebuilds


def _sample_data() -> pd.DataFrame:
    """Small placeholder dataset for rapid UI feedback."""
    return pd.DataFrame([
        {"TeamName": "Lakers", "Season": "2022-23", "MadePlayoffs": 1},
        {"TeamName": "Lakers", "Season": "2023-24", "MadePlayoffs": 0},
        {"TeamName": "Spurs",  "Season": "2022-23", "MadePlayoffs": 0},
        {"TeamName": "Spurs",  "Season": "2023-24", "MadePlayoffs": 0},
    ])


def _run_with_capture(func, *args, **kwargs) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue().strip()


def main() -> None:
    st.set_page_config(page_title="NBA Rebuild Analyzer", layout="wide")
    st.title("NBA Rebuild Analyzer")
    st.write("Fetch standings, clean them, and compute multi-season rebuilds.")

    with st.sidebar:
        st.header("Controls")

        dataset_choice = st.selectbox("Dataset Source", ["Sample Data", "Fetch via API", "Upload CSV"])

        st.subheader("Fetch Settings")
        start_year = st.number_input("Start Year", min_value=2000, max_value=2030, value=2023)
        end_year = st.number_input("End Year", min_value=2000, max_value=2030, value=2023)

        run_clean = st.checkbox("Run cleaning pipeline")
        run_compute = st.checkbox("Compute rebuilds")

    # Data Selection
    if dataset_choice == "Sample Data":
        df = _sample_data()

    elif dataset_choice == "Fetch via API":
        st.info("Fetching through nba_api…")
        output = _run_with_capture(fetch_data.save_standings, start_year, end_year)
        st.code(output)

        # load what was fetched
        file = f"nba_rebuilds/data/standings_{start_year}-{end_year}.csv"
        df = pd.read_csv(file)

    else:   # Upload
        uploaded = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
        else:
            st.warning("Upload a file or switch back to Sample Data.")
            df = _sample_data()

    # Data preview
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    # Clean Pipeline
    if run_clean:
        st.subheader("Cleaning Output")
        st.write("No complex cleaning pipeline defined; assuming data is already clean.")
        # You can plug in your cleaning logic if you have one.

    # Rebuild analysis
    if run_compute:
        st.subheader("Rebuild Analysis Results")
        rebuilds_df = rebuilds.compute_rebuilds(df)
        st.dataframe(rebuilds_df, use_container_width=True)

        if rebuilds_df.empty:
            st.info("No rebuilds detected with current data.")
        else:
            st.success("Rebuilds computed!")

    st.markdown("---")
    st.caption("Customize this app for your final deliverable. Include visuals if relevant.")


if __name__ == "__main__":
    main()
