# Arbitrage Sports Betting
This project consists of web scrapers designed to extract, aggregate, and format sports betting data from online sportsbooks into JSON files using Python’s BeautifulSoup library.

It also includes a script that processes the JSON files from the web scrapers to analyze the data and identify potential arbitrage betting opportunities. These opportunities allow bettors to place multiple bets on different outcomes to guarantee a profit regardless of the outcome.

### [Unreleased]
- Ongoing improvements and updates.
  
### [09/09/2024] - Added scraping for football, basketball, baseball, and mma.
- Added `dk_game_odds_20240909_010358.json` as example of the JSON output from the latest update.
- Added `dk_webscraper.py` as initial DK web scraper with functionality for sports that follow the spread/total/moneyline table format.

### [09/08/2024] - Project initialization
- Added `dk_nfl_webscraper.py` as baseline web scraper for DraftKings.
