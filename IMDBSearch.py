from IMDB import IMDB
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--director", type=str, nargs='+', default=[])
parser.add_argument("-a", "--actor", type=str, nargs='+', default=[])
parser.add_argument("-t", "--title", type=str)
parser.add_argument("-y", "--year", type=int)
parser.add_argument("-g", "--genre", type=str,
choices=[\
'Film-Noir', 'History', 'Biography', 'Fantasy',\
'Thriller', 'Comedy', 'Horror', 'Musical',\
'Drama', 'Mystery', 'Western', 'Music',\
'Animation', 'Sport', 'Crime', 'War', 'Family',\
'Sci-Fi', 'Action', 'Adventure', 'Romance'])

args = parser.parse_args()

search_terms = args.director
if args.title:
    search_terms.insert(0, args.title)
search_terms += args.actor
if args.year is not None:
    search_terms.append(str(args.year))
if args.genre is not None:
    search_terms.append(args.genre)

data = IMDB()
data.search(search_terms)
