# IMDb Scraper

For populating personal database. Able to scrape all movies from IMDb chart page like [top 250 movies](https://www.imdb.com/chart/top/) and other pages with similar html structure.

## Usage
1. Change the url link of `source = requests.get('https://www.imdb.com/chart/top/')` in `imdb_scraper.py` to any of other charts (e.g. [Most Popular Movies](https://www.imdb.com/chart/moviemeter/) or [Most Popular TV](https://www.imdb.com/chart/tvmeter/))
2. Change the output csv file name as desired
3. Run `python3 imdb_scraper.py` (Mac) and `python imdb_scraper.py` (Windows)

## Sample Data
* [Top 250 Movies](./top250.csv)
* [Most Popular Movies](./popular100.csv)