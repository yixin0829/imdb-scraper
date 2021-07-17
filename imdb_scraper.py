from bs4 import BeautifulSoup, SoupStrainer
import requests
import re


# needed data: 1) Name, 2) year, 3) director(s), 4) genre (comma separated), 5) Link
# csv file fields: 1) Type, 2) Name, 3) Year, 4) Director, 5) Genre, 6) Rating(1-10), 7) Link

source = requests.get('https://www.imdb.com/chart/')
# source = requests.get('https://www.imdb.com/chart/moviemeter/')
# Extract the html text in source (i.e. the website we try to scrap data from)
content = source.content

# Creating a soup object based on the content of the source 
# Note: using lxml’s HTML parser - very fast. Or can use Python's html.parser - a bit slower
soup = BeautifulSoup(content, features='lxml')

# init a csv file
f = open('top250.csv', 'w')
# f = open('popular100.csv', 'w')
headers = "Type,Name,Year,Director(s),Genre(s),Rating(1-10),Link\n"
f.write(headers)

count = 1
all_movies = soup.find_all(class_='titleColumn')
ttl_count = len(all_movies)
for link in all_movies:
    row = [None] * 7
    a_tag = link.find('a')
    if not a_tag: # error handling to avoid NoneType
        continue

    # populate the fields
    row[0] = 'Film' # type
    row[1] = a_tag.get_text() # Name
    row[2] = link.find('span').get_text()[1:-1] # Year
    row[6] = 'https://www.imdb.com' + a_tag.get('href') # URL
    row[5] = '0'

    subpage = requests.get(row[6])
    little_soup = BeautifulSoup(subpage.content, features='lxml')
    ## director name(s)
    directors = '' # temp holder to be written into row list
    director_box = little_soup.find(text='Director')
    if not director_box: # multiple directors
        director_box = little_soup.find(text='Directors')
    # print(direct_atags)
    try:
        for dlink in director_box.parent.parent.find_all('a'):
            if len(directors) == 0: # empty string
                directors = dlink.get_text()
            else:
                directors = directors + ',' + dlink.get_text()
            
        row[3] = '\"' + directors + '\"'
    except AttributeError:
        row[3] = ''

    ## genre(s)
    genre_list = little_soup.find(class_='ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL')
    if not genre_list: # different layout, use different class name locator(e.g. see 19/250 SEven Samurai)
        genre_list = little_soup.find(class_='ipc-chip-list GenresAndPlot__OffsetChipList-cum89p-5 dMcpOf')
    genres = '' # temp holder to be written into row list
    try:
        for glink in genre_list.find_all('a'):
            if len(genres) == 0: # empty string
                genres = glink.get_text()
            else:
                genres = genres + ',' + glink.get_text()

        row[4] = '\"' + genres + '\"'
    except AttributeError:
        row[4] = ''

    print(f'{count} out of {ttl_count}: {row}')
    # write joined row into the csv file
    f.write(','.join(row) + '\n')

    count += 1

f.close()
