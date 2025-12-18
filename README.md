# nba_rebuild_project

## published github site:
https://mitchster21.github.io/nba_rebuild_project/


The repository bundles a Python package, Quarto site, automated tests, and two Streamlit prototypes for analyzing NBA rebuilds and predicting playoff returns.

## Quick start
Clone the repository, install dependencies, and run tests:
```bash
git clone https://github.com/mitchster21/nba_rebuild_project.git
cd nba_rebuild_project
pip install -e .
uv sync
uv run pytest
```

# Streamlit App: NBA Analytics Suite
Run this command to launch the full NBA Analytics Suite with both the Rebuild Analyzer and Playoff Predictor:
```bash
uv run streamlit run streamlit_app.py
```

## Rebuild Analyzer

-Select a range of NBA seasons.

-Preview multi-season standings data.

-Aggregate performance metrics by team (Team Summary) or view raw season data (Raw Season Data).

-Click Compute Rebuilds to detect rebuild periods for the selected years.

-Tip: Fetching via the NBA API can be slow or restricted; rely on pre-fetched CSVs when possible.

## Playoff Predictor

-Estimate how many years a team may take to return to the playoffs based on roster continuity and player features.

-Generate predictions for individual teams or run batch predictions.

-View feature importance to understand model behavior.

-Adjust filters and toggles to test different team indicators.

## Advanced users 
You can edit individual Streamlit scripts directly:
```bash
pages/1_Rebuild_Analyzer.py
pages/2_Playoff_Predictor.py
```

# Core modules

- fetch_data.py — fetch and persist NBA standings CSVs across seasons.

- train_model.py — build and evaluate regression models predicting years until playoff return.

- predictor.py — load trained models and expose prediction APIs.

- 1_Rebuild_Analyzer.py — Streamlit app for standings aggregation and rebuild analysis.

- 2_Playoff_Predictor.py — Streamlit app for playoff return predictions.

- eda.ipynb — exploratory notebook for standings data and Gantt chart visualization.

## Quarto site

Rebuild the public site (including the technical report placeholder) with:

```bash
cd docs
uv run quarto render # build site 
uv run quarto preview # serve locally
```

while authoring docs.

# Data and models

- Season standings CSV's are written under src/nba_rebuilds/data/standings_{season}.csv.

- Trained models, scalers, and feature lists are saved under src/nba_rebuilds/data/models.

# Tests

Automated tests validate data fetching, transformation, and model training. Run them with:

```bash
uv run pytest
```

- This structure makes it easy to:

    - Fetch and preprocess NBA data

    - Analyze rebuild timelines

    - Train and evaluate predictive models

    - Serve interactive dashboards

    - Publish technical documentation via Quarto