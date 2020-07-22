import pandas as pd
import re
         
def clean_text(string):
    '''
    Name cleaning to remove [], (), *
    '''
    
    string = re.sub('\[.*?\]|[0-9*()^]', '', string)
    string = string.strip()

    return string

def name_change(final_df):
    '''
    Name change for certain players3
    '''
    final_df['Players'] = final_df['Players'].replace('Akeem Olajuwon', 'Hakeem Olajuwon')
    # Amare to A'mare
    final_df['Players'] = final_df['Players'].replace("Amare Stoudemire", "Amar'e Stoudemire")
    # Ron Artest to Metta World Peace
    final_df['Players'] = final_df['Players'].replace('Ron Artest', 'Metta World Peace')
    
    return final_df

def all_stars(year):
    '''
    Determine players that are all stars for a given year
    '''
    df = pd.read_html('https://www.basketball-reference.com/allstar/NBA_{}.html'.format(year))
    
    east_players = df[1]
    west_players = df[2]
    
    # lower column names
    east_players.columns = east_players.columns.get_level_values(1)
    west_players.columns = west_players.columns.get_level_values(1)
    
    # create a dataframe
    all_stars = pd.DataFrame()
    
    players = pd.Series(list(east_players['Starters']) + list(west_players['Starters']))
    
    all_stars['Players'] = players
    all_stars['Season'] = year
    
    rows_to_drop = ['Reserves', 'Team Totals']
    
    all_stars = all_stars[~all_stars['Players'].isin(rows_to_drop)].dropna()
    
    return all_stars
    
def all_nba_team():
    """
    Scrape the players who are on the All NBA team
    """
    
    df = pd.read_html('https://en.wikipedia.org/wiki/All-NBA_Team')# Read html
    df = df[7].copy(deep = True) # Get exact table 
    
    multiindex_names = list(df.columns.levels[0])
    multiindex_names.remove('Season')
   
    df.columns = [f'{i}_{j}' for i, j in df.columns]
    team_cols = [col for col in df.columns if 'Teams' in col]
    
    df = df[df.columns.difference(team_cols)].copy(deep = True)
    
    df['first_nba_team'] = '1st'
    df['second_nba_team'] = '2nd'
    df['third_nba_team'] = '3rd'
    
    df['First team_Players'] = df['First team_Players'].apply(clean_text)
    df['Second team_Players'] = df['Second team_Players'].apply(clean_text)
    df['Third team_Players'] = df['Third team_Players'].apply(clean_text)
    
    #split into 3 dfs
    first_team = df[['First team_Players', 'Season_Season', 'first_nba_team']]
    second_team = df[['Second team_Players', 'Season_Season', 'second_nba_team']]
    third_team = df[['Third team_Players', 'Season_Season', 'third_nba_team']]
    
    columns = ['Players', 'Season','All nba team']

    first_team.columns = columns
    second_team.columns = columns
    third_team.columns = columns

    dfs = [first_team, second_team, third_team]
    
    final_df = pd.concat(dfs).reset_index(drop = True)
    
    final_df = name_change(final_df)
    
    return final_df



    
        
