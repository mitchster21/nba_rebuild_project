# nba_rebuild_project

## Published GitHub Site
https://mitchster21.github.io/nba_rebuild_project/

---

## Overview

This repository provides the `nba_rebuilds` Python package and Streamlit applications for:
- Fetching NBA standings data
- Analyzing multi-season rebuild trends
- Predicting how long teams may take to return to the playoffs

No prior knowledge of the internal codebase is required.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/mitchster21/nba_rebuild_project.git
cd nba_rebuild_project
pip install -e .
uv sync
```

Run automated tests to validate the setup:

```bash
uv run pytest
```

---

## Fetch NBA Standings Data

Standings data can be fetched using the public NBA API or loaded from pre-downloaded CSV files.

To fetch manually:

```bash
uv run python -m nba_rebuilds.fetch_data --start 2010 --end 2023 --type standings
```

Season standings are saved under:

```bash
src/nba_rebuilds/data/
```

---

## Launch Streamlit App

Run the entire NBA Analytics Suite (both Rebuild Analyzer and Playoff Predictor) with one command:

```bash
uv run streamlit run streamlit_app.py
```

---

## Rebuild Analyzer (Streamlit App)

- Select a range of NBA seasons.
- Preview combined multi-season standings data.
- Aggregate performance metrics by team (**Team Summary**) or view raw season data (**Raw Season Data**).
- Click **Compute Rebuilds** to see detected rebuilds for the selected years.
- **Tip:** Fetching via the NBA API can be slow or restricted; using pre-fetched CSV files in `src/nba_rebuilds/data/` is recommended.

---

## Playoff Predictor (Streamlit App)

- Estimate how many years a team may take to return to the playoffs based on roster continuity and player features.
- Generate predictions for individual teams or run batch predictions.
- View feature importance to understand model behavior.
- Adjust toggles and filters to experiment with different team indicators.

---

## Advanced Users

You can edit individual Streamlit scripts directly:

```bash
pages/1_Rebuild_Analyzer.py
pages/2_Playoff_Predictor.py
```

---

## Core Modules

- **fetch_data.py** — fetch and persist NBA standings CSVs across seasons  
- **train_model.py** — build and evaluate regression models predicting years until playoff return  
- **predictor.py** — load trained models and expose prediction APIs  
- **1_Rebuild_Analyzer.py** — Streamlit app for standings aggregation and rebuild analysis  
- **2_Playoff_Predictor.py** — Streamlit app for playoff return predictions  
- **eda.ipynb** — exploratory notebook for standings data and Gantt chart visualization  

---

## Data and Models

- Season standings CSVs are written under `src/nba_rebuilds/data/standings_{season}.csv`  
- Trained models, scalers, and feature lists are saved under `src/nba_rebuilds/data/models`  

---

## Tests

Automated tests validate data fetching, transformation, and model training:

```bash
uv run pytest
```

---

This structure makes it easy to:
- Fetch and preprocess NBA data
- Analyze rebuild timelines
- Train and evaluate predictive models
- Serve interactive dashboards
```

---