"""Streamlit app for NBA rebuild analysis."""

import io
from contextlib import redirect_stdout
import pandas as pd
import streamlit as st
from pathlib import Path

from nba_rebuilds import fetch_data, rebuilds

def aggregate_by_team(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate multi-season standings into one row per team."""
    return (
        df.groupby("TeamName")
        .agg(
            Seasons=("SeasonID", "nunique"),
            AvgWins=("Wins", "mean"),
            AvgWinPct=("WinPct", "mean"),
            PlayoffAppearances=("MadePlayoffs", "sum"),
            PlayoffRate=("MadePlayoffs", "mean"),
            FirstSeason=("SeasonID", "min"),
            LastSeason=("SeasonID", "max"),
        )
        .reset_index()
        .sort_values("AvgWinPct", ascending=False)
    )


def _run_with_capture(func, *args, **kwargs) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue().strip()


def load_season_csv(year: int) -> pd.DataFrame:
    """Load a standings CSV for a given NBA year (2021 = loads 2020-21 season)."""
    season_start = year - 1
    season_end = str(year)[-2:]
    season_id = f"{season_start}-{season_end}"

    # Project root is where 'src/nba_rebuilds/data/' lives
    PROJECT_ROOT = Path(__file__).resolve().parent.parent  # adjust if needed
    file_path = PROJECT_ROOT / "src" / "nba_rebuilds" / "data" / f"standings_{season_id}.csv"

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)
    df["SeasonID"] = season_id
    return df



def main() -> None:
    st.title("NBA Rebuild Analyzer")
    st.write("Fetch standings, view multi-season data, and analyze rebuild patterns.")

    with st.sidebar:
        st.header("Controls")

        start_year = st.number_input(
            "Start NBA Year", min_value=2000, max_value=2030, value=2010
        )
        end_year = st.number_input(
            "End NBA Year", min_value=2000, max_value=2030, value=2023
        )

        fetch_button = st.button("Fetch Standings via nba_api")
        compute_button = st.button("Compute Rebuilds")
        view_mode = st.radio("Data View", ["Team Summary", "Raw Season Data"])

    # FETCH DATA (multi-season)
    if fetch_button:
        st.info("Fetching standings from nba_api...")
        output = _run_with_capture(fetch_data.save_standings, start_year, end_year)
        st.code(output)

    # LOAD ALL SEASONS INTO ONE DF
    st.subheader("Multi-Season Data Preview")

    dfs = []
    for year in range(start_year, end_year + 1):
        try:
            df_year = load_season_csv(year)
            dfs.append(df_year)
        except FileNotFoundError:
            st.warning(f"Missing season file for {year}. Fetch it first.")

    if len(dfs) == 0:
        st.stop()

    df_all = pd.concat(dfs, ignore_index=True)

    st.subheader("Data Preview")

    if view_mode == "Team Summary":
        df_team = aggregate_by_team(df_all)
        st.dataframe(df_team, use_container_width=True)
    else:
        st.dataframe(df_all, use_container_width=True)

    # REBUILD ANALYSIS
    if compute_button:
        st.subheader("Rebuild Analysis")

        rebuilds_df = rebuilds.compute_rebuilds(df_all)
        st.dataframe(rebuilds_df, use_container_width=True)

        if rebuilds_df.empty:
            st.info("No rebuilds detected with current parameters.")
        else:
            st.success("Rebuilds computed!")


if __name__ == "__main__":
    main()