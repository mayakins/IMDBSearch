from bs4 import BeautifulSoup
import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--director", type=str, nargs='+', default=[])
parser.add_argument("-a", "--actor", type=str, nargs='+', default=[])
args = parser.parse_args()

print(args.director)
print(args.actor)



# url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&view=advanced'

# one table from key -> movie name (key can be the ranking from 1-1000)
# another table from key_word -> movie ids
# another table from movie_id to unordered_set of key_words
movie_map = {}
keyword_map = {}
m_id = 1

## TODO: update this with full 1000 movie list not just first page
url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start=1'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
thing = soup.find(class_='lister list detail sub-list')
# print thing
items = thing.find_all(class_='lister-item mode-advanced')
# items = thing.select(".lister-item mode-advanced .lister-item-content")
# print items
for item in items:
    title = item.h3.a.text
    year = item.find(class_="lister-item-year text-muted unbold").text[1:-1]
    genre = item.p.find(class_="genre").text[1:-1]
    # cert = item.p.find(class_="certificate").text
    votes = item.find(class_="sort-num_votes-visible")
    people = votes.find_previous('p')
    people = people.find_all('a')
    # print(people)
    keywords = list(map(lambda p: p.text, people))
    keywords.extend([title, year])
    # print(keywords)

    # print keywords
    for key in keywords:
        if key in keyword_map:
            keyword_map[key].add(m_id)
        else:
            keyword_map[key] = {m_id}

    movie_map[m_id] = title
    # print title
    # # print genre
    # for p in people:
    #     print p.text
    # print year
    # print cert
    m_id = m_id + 1
# print items
# period_tags = seven_day.select(".tombstone-container .period-name")
# print soup.prettify()
# print movie_map
# print(keyword_map)
# print(movie_map)

# search = input("Type something to test this out: ")

###### Search
search_terms = args.director + args.actor
if len(search_terms) > 0:
    if search_terms[0] not in keyword_map:
        print(search_terms[0], "not found")
        sys.exit()
    res = keyword_map[search_terms[0]]
    # print(first)
    if len(search_terms) > 1:
        results = list(map(lambda keyword: keyword_map.get(keyword), keys[1:]))
        for k in search_terms[1:]:
            if k not in keyword_map:
                print(k, "not found")
                sys.exit()
            res = res.intersection(keyword_map[k])
            if len(k) == 0:
                break
    for k in res:
        print(movie_map[k])
