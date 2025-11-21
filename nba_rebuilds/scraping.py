from nba_api.stats.endpoints import leaguestandings
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

def get_standings(season="2023-24"):
    standings = leaguestandings.LeagueStandings(season=season)
    df = standings.get_data_frames()[0]

    # Rename to match your workflow
    df = df.rename(columns={
        'WINS': 'Wins',
        'LOSSES': 'Losses',
        'WinPCT': 'WinPct'
    })

    df['Season'] = season

    # Top 8 per conference make playoffs
    df['MadePlayoffs'] = 0
    df.loc[df.groupby('Conference').cumcount() < 8, 'MadePlayoffs'] = 1

    return df[['TeamName', 'Conference', 'Wins', 'Losses', 'WinPct', 'Season', 'MadePlayoffs']]

def save_standings(season="2023-24"):
    df = get_standings(season)
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / f"standings_{season}.csv"
    df.to_csv(path, index=False)
    print(f"Saved: {path}") 