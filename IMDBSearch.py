from IMDB import IMDB
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--director", type=str, nargs='+', default=[])
parser.add_argument("-a", "--actor", type=str, nargs='+', default=[])
parser.add_argument("-t", "--title", type=str)
args = parser.parse_args()

search_terms = args.director
if args.title:
    search_terms.insert(0, args.title)
search_terms += args.actor

data = IMDB()
data.search(search_terms)
