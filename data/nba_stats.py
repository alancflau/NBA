from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def player_stats(season, stat_type):
    '''
    Parameters:
    season: year of nba season
    stat_type: stats of interest: per_game, advaned
    
    '''
    url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(season, stat_type)
    html = urlopen(url)
    soup = BeautifulSoup(html)
    
    soup.findAll('tr', limit = 2)# use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:] # remove rank
    
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
    
    stats = pd.DataFrame(player_stats, columns = headers)
    
    return stats


def player_stats_seasons(season_start, season_end):
    
    all_dfs = []
    for year in range(season_start, season_end):
        df = player_stats(season_start)
        df['Season'] = season_start
        all_dfs.append(df)
    
    result = pd.concat(all_dfs)
    
    return result