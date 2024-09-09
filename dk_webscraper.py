import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


# Replacing the unicode minus for JSON readability.
def replace_minus(text):
    if text:
        return text.replace('\u2212', '-')
    return text


# Function to scrape the DK leagues with Spread/Total/ML format for games.
def scrape_stm_games(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    game = []
    games = {}
    rows = []
    team_no = 0
    current_game = ""
    
    # Find all table bodies in the table representing days.
    days = soup.find_all('tbody', class_='sportsbook-table__body')

    # Find all rows in table bodies representing teams.
    for day in days:
        rows += day.find_all('tr')

    for row in rows:
        team_no += 1
        
        # Team of current row.
        team_name = row.find('div', class_='event-cell__name-text').text.strip()
        
        # Columns with Game Odds.
        columns = row.find_all('td', class_='sportsbook-table__column-row')
        
        # First column - Spread and Spread Odds.
        spread_cell = columns[0]
        if spread_cell.find('div', class_='sportsbook-empty-cell'):
            spread = 'N/A'
            spread_odds = 'N/A'
        else:
            spread = spread_cell.find('span', class_='sportsbook-outcome-cell__line').text.strip()
            spread_odds = spread_cell.find('span', class_='sportsbook-odds').text.strip()
            spread_odds = replace_minus(spread_odds)

        # Second column - Over/Under (ou) and Odds.
        ou_cell = columns[1]
        if ou_cell.find('div', class_='sportsbook-empty-cell'):
            ou = 'N/A'
            ou_odds = 'N/A'
        else:
            ou = ou_cell.find('div', class_='sportsbook-outcome-cell__body').get('aria-label')
            ou_odds = ou_cell.find('span', class_='sportsbook-odds').text.strip()
            ou_odds = replace_minus(ou_odds)

        # Third column - Moneyline (ml).
        ml_cell = columns[2]
        if ml_cell.find('div', class_='sportsbook-empty-cell'):
            ml = 'N/A'
        else:
            ml = ml_cell.find('span', class_='sportsbook-odds').text.strip()
            ml = replace_minus(ml)

        # Add game data to list.
        if team_no % 2 == 1:
            current_game += team_name + " vs "
            
            game.append({
                'team_name': team_name,
                'spread': spread,
                'spread_odds': spread_odds,
                'ou': ou,
                'ou_odds': ou_odds,
                'ml': ml
            })
        else:
            current_game += team_name
            
            game.append({
                'team_name': team_name,
                'spread': spread,
                'spread_odds': spread_odds,
                'ou': ou,
                'ou_odds': ou_odds,
                'ml': ml
            })
            
            games.update({
                current_game: game
            })
            current_game = ""
            game = []

    return games


if __name__ == "__main__":
    # DraftKings URLs for various sports and leagues.
    
    # Football.
    ncaaf = 'https://sportsbook.draftkings.com/leagues/football/ncaaf'
    nfl = 'https://sportsbook.draftkings.com/leagues/football/nfl'
    
    # Baseball.
    mlb = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'

    # Basketball.
    nba = 'https://sportsbook.draftkings.com/leagues/basketball/nba'
    wnba = 'https://sportsbook.draftkings.com/leagues/basketball/wnba'

    # MMA.
    ufc = 'https://sportsbook.draftkings.com/leagues/mma/ufc'
    pfl = 'https://sportsbook.draftkings.com/leagues/mma/pfl'
    bellator = 'https://sportsbook.draftkings.com/leagues/mma/bellator'
    dwcs = 'https://sportsbook.draftkings.com/leagues/mma/dana-white%E2%80%99s-contender-series'

    # Scrape game data from DK (Need to update for asynchronicity).
    ncaaf_game_data = scrape_stm_games(ncaaf)
    nfl_game_data = scrape_stm_games(nfl)
    mlb_game_data = scrape_stm_games(mlb)
    nba_game_data = scrape_stm_games(nba)
    wnba_game_data = scrape_stm_games(wnba)
    ufc_data = scrape_stm_games(ufc)
    dwcs_data = scrape_stm_games(dwcs)
    bellator_data = scrape_stm_games(bellator)
    pfl_data = scrape_stm_games(pfl)

    # Combine all data (Need to update for leagues/sports that don't follow stm format).
    dk_game_data = {
        "nfl": nfl_game_data,
        "ncaaf": ncaaf_game_data,
        "mlb": mlb_game_data,
        "nba": nba_game_data,
        "wnba": wnba_game_data,
        "ufc": ufc_data,
        "dwcs": dwcs_data,
        "bellator": bellator_data,
        "pfl": pfl_data
    }

    # Timestamped filename.
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'dk_game_odds_{timestamp}.json'

    # Save data to JSON.
    with open(filename, 'w') as json_file:
        json.dump({'DK_game_data': dk_game_data}, json_file, indent=4)