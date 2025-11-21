import pandas as pd

def compute_rebuilds(all_standings):
    # Ensure numeric SeasonStart
    all_standings['SeasonStart'] = all_standings['Season'].str.split('-').str[0].astype(int)

    rebuilds = []
    teams = all_standings['TeamName'].unique()

    for team in teams:
        team_df = all_standings[all_standings['TeamName'] == team].sort_values('SeasonStart').reset_index(drop=True)
        in_rebuild = False
        start_season = None
        start_year = None

        for i in range(1, len(team_df)):
            prev = team_df.iloc[i-1]
            curr = team_df.iloc[i]

            prev_playoff = prev['MadePlayoffs']
            curr_playoff = curr['MadePlayoffs']

            # Rebuild starts
            if prev_playoff == 1 and curr_playoff == 0 and not in_rebuild:
                in_rebuild = True
                start_season = curr['Season']
                start_year = curr['SeasonStart']

            # Rebuild ends
            if in_rebuild and curr_playoff == 1:
                rebuilds.append({
                    'Team': team,
                    'Start': start_season,
                    'End': curr['Season'],
                    'Length': curr['SeasonStart'] - start_year + 1
                })
                in_rebuild = False
                start_season = None
                start_year = None

    return pd.DataFrame(rebuilds)
