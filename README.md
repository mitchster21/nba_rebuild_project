# nba_rebuild_project

## published github site:
https://mitchster21.github.io/nba_rebuild_project/


The repository bundles a Python package, Quarto site, automated tests, and two Streamlit prototypes for analyzing NBA rebuilds and predicting playoff returns.

## Quick start

```bash
uv sync
uv run pytest
```

# Streamlit prototypes

## Rebuild Analyzer

- Edit src/nba_rebuilds/1_Rebuild_Analyzer.py to adjust data sources or rebuild logic.

- Launch the UI with:

```bash
uv run streamlit run src/nba_rebuilds/1_Rebuild_Analyzer.py
```

- Use the sidebar controls to:

    - Fetch standings via fetch_data.save_standings

    - Preview multi-season data

    - Aggregate by team

    - Run rebuild computations and view results

## Playoff Predictor

- Edit src/nba_rebuilds/2_Playoff_Predictor.py to customize predictor behavior or visuals.

- Launch the UI with:

```bash
uv run streamlit run src/nba_rebuilds/2_Playoff_Predictor.py
```

- The app loads a trained model via PlayoffPredictor and provides:

    - Single-team predictions

    - Batch predictions

    - Feature importance visualization

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
uv run quarto render
```

Serve locally via:

```bash
uv run quarto preview
```

while authoring docs.

# Data and models

- Season standings are written under src/nba_rebuilds/data/standings_{season}.csv.

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