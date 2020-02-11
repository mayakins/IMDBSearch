# IMDBSearch

## Usage

This script takes the top 1000 IMDB Movies(https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating&view=simple) and creates a search engine on different fields related to the movies. This search engine will return a list of movies titles that match your search results.

Please ensure you are using Python3 to run this script.

Hear is an excerpt from the help:
```
usage: IMDBSearch.py [-h] [-d DIRECTOR [DIRECTOR ...]] [-a ACTOR [ACTOR ...]] [-t TITLE]
                     [-y YEAR]
                     [-g {Film-Noir,History,Biography,Fantasy,Thriller,Comedy,Horror,Musical,Drama,Mystery,Western,Music,Animation,Sport,Crime,War,Family,Sci-Fi,Action,Adventure,Romance}]
```

This search can take in directors, actors, a movie title, year and genre. It must take in at least one search terms to return results.

Here is an example search for comedy movies Brad Pitt is in:
```
IMDBSearch.py -g Comedy -a "Brad Pitt"
```
which will return the following movies:
```
The Big Short
Snatch
Once Upon a Time... in Hollywood
```

Here is another example searching for movies directed by Frank Darabont in 1994:
```
IMDBSearch.py -d "Frank Darabont" -y 1994
```
which will return the following movie:
```
The Shawshank Redemption
```

## Design
IMDBSearch uses Beautiful Soup library to parse the HTML for the IMDB top 1000 movie list. 

It uses to hash maps: 
movies(movie_id -> movie_title)
keywords(keyword -> set{movie_ids})

It extracts the movie title and maps it to a id number(the ranking of the movie in the top 1000 list) and puts this into the movies hash map. It extracts title, director, actors, genres, and release year and uses these as keys to the keywords hash map and maps these keywords to the movie id.

To search, it will take the intersection of all sets of given keywords in the keywords map. Given this list of movie ids, it map these back to movie titles using the movies map.

Example: IMDBSearch.py -d "Frank Darabont" -y 1994
```
keywords["Frank Darabont"] ∩ keywords[1994] => [1] => ["The Shawshank Redemption"]
```

## Limitations
**Search Term Separation**

I have limited the scope of this search by requiring users to pass in each search keyword separately. If users could pass in any search phrase, I would need to figure out how to break down this phrase into separate search terms.

**Exact Match Keywords**

Search terms must be an exact match. If you searched just for actor "Pitt", you would not get back movies with Brad Pitt. You must explicitly search "Brad Pitt"

**Limited Filters**

I am only storing the actors, directors, movie release year, title and genre.

## Next steps
**Reusing crawled data:**
Currently, running the script will crawl the IMDB top 1000 list and put this into a data structure, then search for your search terms. If you wanted to search multiple times, it would be nice if you didn't have to crawl IMDB and build this data structure again. If I had more time, I would modify this script to keep running until the user specifies they want to exit. This way I can keep searching and using the same data structure in the same session without having to keep unnecessarily rebuilding this data structure. This would require a change to my search input design, as it currently just takes the search terms as script arguments.

**Allowing search of plain string:**
Currently, I require you to split your search by search term type. This allows me to take out the guess work about where to break up search keywords. It would be a simpler, more intuitive user experience if this could just take in a search phrase as one string.

**Allowing pieces non full-names:**
Currently, you can only search full names and titles. This could be solved using the current data structure by breaking down each piece of data into separate words (excluding filler words like the, of, at) and putting those keywords into our search hashmap. However, this would greatly increase the size of our data structure and create a lot of duplicate data storage. For example, "Brad" and "Pitt" would both have lists to all Brad Pitt movies.

**Differentiate data by type:**
Currently, search inputs are separated by type (actor, director, title, year, genre). However, this separation is just used to split search terms and specify what types of information would return meaningful results. Each search term is treated the same as in it will search the movie_keywords table for the matching keyword. Say I was searching for movies with the actor "Brad Pitt", but there was also a movie about Brad Pitt called "Brad Pitt". The movie "Brad Pitt" would also be returned in the search. I don't think this is a big issue, since if you were searching for Brad Pitt, you probably wouldn't be surprised to see Brad Pitt the movie either. However, if this was a concern and we wanted to stick with this type differentiated seach design, we could store each seach term with their respective types like Brad Pitt_actor or Brad Pitt_movie. Alternatively, we could have separate tables for each type of data like directors, actors, etc. However, this would complicate code as we would have to check the type each time we stored or searched data, but could cleanly separate these types.

**Add input sanitizion:**
Currently a keyword has to be an exact match to find results. It would be nice to have som input sanitization so search terms like "brad pitt", "Brad Pitt" and "  Brad Pitt  " would all return the same result.

**Search for year range instead of year:**
Currently, the only date features you can search for is a specific year. I think it would be more likely that a user would search for a movie in a certain date range than to know the specific release year of a movie. To search for a date range, I would need some data structure that stored a sorted list of all movies by date.

