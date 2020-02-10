from bs4 import BeautifulSoup
import requests


class IMDB:
    movie_map = {}
    keyword_map = {}

    def __init__(self):
        m_id = 1
        ## TODO: update this with full 1000 movie list not just first page
        url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start=1'
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        thing = soup.find(class_='lister list detail sub-list')
        items = thing.find_all(class_='lister-item mode-advanced')

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
                if key in self.keyword_map:
                    self.keyword_map[key].add(m_id)
                else:
                    self.keyword_map[key] = {m_id}

            self.movie_map[m_id] = title
            # print title
            # # print genre
            # for p in people:
            #     print p.text
            # print year
            # print cert
            m_id = m_id + 1

    def search(self, search_terms):
        if len(search_terms) > 0:
            if search_terms[0] not in self.keyword_map:
                print(search_terms[0], "not found")
                return
            res = self.keyword_map[search_terms[0]]

            if len(search_terms) > 1:
                for k in search_terms[1:]:
                    if k not in self.keyword_map:
                        print(k, "not found")
                        return
                    res = res.intersection(self.keyword_map[k])
                    if len(k) == 0:
                        break
            for k in res:
                print(self.movie_map[k])
