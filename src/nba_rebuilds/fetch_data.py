import argparse
import os
import time
from nba_rebuilds.scraping import get_standings

DATA_DIR = "nba_rebuilds/data"

def save_standings(start, end):
    os.makedirs(DATA_DIR, exist_ok=True)

    for year in range(start, end + 1):
        # NBA API seasons are formatted like 2009-10, 2010-11
        season_start = year - 1
        season_end = str(year)[-2:]
        season_id = f"{season_start}-{season_end}"

        print(f"Fetching standings for {season_id}...")
        df = get_standings(season_id)

        # Rename columns to match workflow
        df = df.rename(columns={
            'WINS': 'Wins',
            'LOSSES': 'Losses',
            'WinPCT': 'WinPct'
        })
        df['Season'] = season_id

        # Top 8 teams per conference make playoffs
        df['MadePlayoffs'] = 0
        df.loc[df.groupby('Conference').cumcount() < 8, 'MadePlayoffs'] = 1

        # Pause between API calls
        time.sleep(1)

        outfile = os.path.join(DATA_DIR, f"standings_{season_id}.csv")
        df.to_csv(outfile, index=False)
        print(f"Saved → {outfile}")

    print("Done!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--type", type=str, required=True)
    args = parser.parse_args()

    if args.type == "standings":
        save_standings(args.start, args.end)
    else:
        raise ValueError("Unknown type. Use: standings")

if __name__ == "__main__":
    main()
