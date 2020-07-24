# Important variables:
#     movie_db: list of 4-tuples (imported from movies.py)
#     pa_list: list of pattern-action pairs (queries)
#       pattern - strings with % and _ (not consecutive)
#       action  - return list of strings

# THINGS TO ASK THE MOVIE CHAT BOT:
# what movies were made in _ (must be date, because we don't have location)
# what movies were made between _ and _
# what movies were made before _
# what movies were made after _
# who directed %
# who was the director of %
# what movies were directed by %
# who acted in %
# when was % made
# in what movies did % appear
# bye

#  Include the movie database, named movie_db
from movies import movie_db
from match import match
from typing import List, Tuple, Callable, Any

# The projection functions, that give us access to certain parts of a "movie" (a tuple)
def get_title(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[0]


def get_director(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[1]


def get_year(movie: Tuple[str, str, int, List[str]]) -> int:
    return movie[2]


def get_actors(movie: Tuple[str, str, int, List[str]]) -> List[str]:
    return movie[3]


# Below are a set of actions. Each takes a list argument and returns a list of answers
# according to the action and the argument. It is important that each function returns a
# list of the answer(s) and not just the answer itself.


def title_by_year(matches: List[str]) -> List[str]:
    """Finds all movies made in the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of movie titles made in the passed in year
    """
    year = int(matches[0])

    def movie_made_in_year(movie: Tuple[str,str, int, List[str]]) -> bool:
        return year == get_year(movie)

    lom = filter(movie_made_in_year, movie_db)
    lot = (map(get_title, lom))
    return list(lot)


def title_by_year_range(matches: List[str]) -> List[str]:
    """Finds all movies made in the passed in year range

    Args:
        matches - a list of 2 strings, the year beginning the range and the year ending
            the range. For example, to get movies from 1991-1994 matches would look like
            this - ["1991", "1994"] Note that these years are passed as strings and
            should be converted to ints.

    Returns:
        a list of movie titles made during those years, inclusive (meaning if you pass
        in ["1991", "1994"] you will get movies made in 1991, 1992, 1993 & 1994)
    """
    loy = list(range(int(matches[0]),int(matches[-1]) + 1))
    los = list(map(str, loy))
    result = []
    for i in los:
        result = result + title_by_year([i])
    return result
        
        


def title_before_year(matches: List[str]) -> List[str]:
    """Finds all movies made before the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of movie titles made before the passed in year, exclusive (meaning if you
        pass in 1992 you won't get any movies made that year, only before)
    """
    loye = list(map(get_year, movie_db))
    loye.sort()
    s = loye[0]
    res = []
    while s < int(matches[0]):
        start = str(s)
        res = res + title_by_year([start])
        s += 1
    return res


def title_after_year(matches: List[str]) -> List[str]:
    """Finds all movies made after the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of movie titles made after the passed in year, exclusive (meaning if you
        pass in 1992 you won't get any movies made that year, only after)
    """

    years = list(map(get_year, movie_db))
    years.sort()
    end = years[-1]
    n = int(matches[0])
    res = []
    while n <= end:
        res = res + title_by_year([n])
        n += 1
    return res


def director_by_title(matches: List[str]) -> List[str]:
    """Finds director of movie based on title

    Args:
        matches - a list of 1 string, just the title

    Returns:
        a list of 1 string, the director of the movie
    """
    title = matches[0]

    def title_of_movies(movie: Tuple[str,str, int, List[str]]) -> bool:
        return title == get_title(movie)

    lom = filter(title_of_movies, movie_db)
    lot = (map(get_director, lom))
    return list(lot)


def title_by_director(matches: List[str]) -> List[str]:
    """Finds movies directed by the passed in director

    Args:
        matches - a list of 1 string, just the director

    Returns:
        a list of movies titles directed by the passed in director
    """
    director = matches[0]

    def director_of_movies(movie: Tuple[str,str, int, List[str]]) -> bool:
        return director == get_director(movie)

    lom = filter(director_of_movies, movie_db)
    lot = (map(get_title, lom))
    return list(lot)


def actors_by_title(matches: List[str]) -> List[str]:
    """Finds actors who acted in the passed in movie title

    Args:
        matches - a list of 1 string, just the movie title

    Returns:
        a list of actors who acted in the passed in title
    """
    title = matches[0]

    def title_of_movies(movie: Tuple[str,str, int, List[str]]) -> bool:
        return title== get_title(movie)

    lom = filter(title_of_movies, movie_db)
    lot = list(map(get_actors, lom))
    loa = lot[0]
    return loa


def year_by_title(matches: List[str]) -> List[int]:
    """Finds year of passed in movie title

    Args:
        matches - a list of 1 string, just the movie title

    Returns:
        a list of one item (an int), the year that the movie was made
    """
    title = matches[0]
    def title_of_movies(movie: Tuple[str,str, int, List[str]]) -> bool:
        return title== get_title(movie)

    lom = filter(title_of_movies, movie_db)
    lot = list(map(get_year, lom))
    return list(lot)
    


def title_by_actor(matches: List[str]) -> List[str]:
    """Finds titles of all movies that the given actor was in

    Args:
        matches - a list of 1 string, just the actor

    Returns:
        a list of movie titles that the actor acted in
    """
    actor = matches[0]
    def actor_of_movies(movie: Tuple[str,str, int, List[str]]) -> bool:
        for n in get_actors(movie):
            if n == actor:
                return True
    loa = filter(actor_of_movies, movie_db)
    lot = list(map(get_title, loa))
    return lot
def directors_by_year(matches: List[str]) -> List[str]:
    """Finds all the directors who made movies in the passed in year

    Args:
        matches - a list of 1 string, just the year. Note that this year is passed as a
            string and should be converted to an int

    Returns:
        a list of directors who made movies in the passed in year
    """
    year = int(matches[0])

    def movie_made_in_year(movie: Tuple[str,str, int, List[str]]) -> bool:
        return year == get_year(movie)

    lom = filter(movie_made_in_year, movie_db)
    lot = (map(get_director, lom))
    return list(lot)

# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# The pattern-action list for the natural language query system A list of tuples of
# pattern and action It must be declared here, after all of the function definitions
pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what movies were made in _"), title_by_year),
    (str.split("what movies were made between _ and _"), title_by_year_range),
    (str.split("what movies were made before _"), title_before_year),
    (str.split("what movies were made after _"), title_after_year),
    # note there are two valid patterns here two different ways to ask for the director
    # of a movie
    (str.split("who directed %"), director_by_title),
    (str.split("who was the director of %"), director_by_title),
    (str.split("what movies were directed by %"), title_by_director),
    (str.split("who acted in %"), actors_by_title),
    (str.split("when was % made"), year_by_title),
    (str.split("in what movies did % appear"), title_by_actor),
    (str.split("which directors directed movies in _"), directors_by_year),
    (["bye"], bye_action),
]


def search_pa_list(src: List[str]) -> List[str]:
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    num_matches = 0
    result: List[str] = []
    for m in pa_list:
        pattern = m[0]
        matchchecker = match(pattern,src)
        if matchchecker != None:
            num_matches += 1
            actionfunc = m[1]
            result = actionfunc(matchchecker)
        if num_matches != 0 and result == []:
            result = ["No answers"]
        elif num_matches == 0 and result == []:
            result = ["I don't understand"]
    return result

def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or Ctrl-D
    characters and exit gracefully.
    """
    print("Welcome to the movie database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nSo long!\n")


# uncomment the following line once you've written all of your code and are ready to try
# it out. Before running the following line, you should make sure that your code passes
# the existing asserts.
# query_loop()

if __name__ == "__main__":
    assert sorted(title_by_year(["1974"])) == sorted(
        ["amarcord", "chinatown"]
    ), "failed title_by_year test"
    assert sorted(title_by_year_range(["1970", "1972"])) == sorted(
        ["the godfather", "johnny got his gun"]
    ), "failed title_by_year_range test"
    assert sorted(title_before_year(["1950"])) == sorted(
        ["casablanca", "citizen kane", "gone with the wind", "metropolis"]
    ), "failed title_before_year test"
    assert sorted(title_after_year(["1990"])) == sorted(
        ["boyz n the hood", "dead again", "the crying game", "flirting", "malcolm x"]
    ), "failed title_after_year test"
    assert sorted(director_by_title(["jaws"])) == sorted(
        ["steven spielberg"]
    ), "failed director_by_title test"
    assert sorted(title_by_director(["steven spielberg"])) == sorted(
        ["jaws"]
    ), "failed title_by_director test"
    assert sorted(actors_by_title(["jaws"])) == sorted(
        [
            "roy scheider",
            "robert shaw",
            "richard dreyfuss",
            "lorraine gary",
            "murray hamilton",
        ]
    ), "failed actors_by_title test"
    assert sorted(year_by_title(["jaws"])) == sorted(
        [1975]
    ), "failed year_by_title test"
    assert sorted(title_by_actor(["orson welles"])) == sorted(
        ["citizen kane", "othello"]
    ), "failed title_by_actor test"
    assert sorted(search_pa_list(["hi", "there"])) == sorted(
        ["I don't understand"]
    ), "failed search_pa_list test 1"
    assert sorted(search_pa_list(["who", "directed", "jaws"])) == sorted(
        ["steven spielberg"]
    ), "failed search_pa_list test 2"
    assert sorted(
        search_pa_list(["what", "movies", "were", "made", "in", "2020"])
    ) == sorted(["No answers"]), "failed search_pa_list test 3"
    assert sorted(directors_by_year(["1974"])) == sorted(
        ["federico fellini", "roman polanski"]
    ), "failed directors_by_year test"

    assert isinstance(title_by_year(["1974"]), list), "title_by_year not returning a list"
    assert isinstance(title_by_year_range(["1970", "1972"]), list), "title_by_year_range not returning a list"
    assert isinstance(title_before_year(["1950"]), list), "title_before_year not returning a list"
    assert isinstance(title_after_year(["1990"]), list), "title_after_year not returning a list"
    assert isinstance(director_by_title(["jaws"]), list), "director_by_title not returning a list"
    assert isinstance(title_by_director(["steven spielberg"]), list), "title_by_director not returning a list"
    assert isinstance(actors_by_title(["jaws"]), list), "actors_by_title not returning a list"
    assert isinstance(year_by_title(["jaws"]), list), "year_by_title not returning a list"
    assert isinstance(title_by_actor(["orson welles"]), list), "title_by_actor not returning a list"
    assert isinstance(directors_by_year(["1974"]), list), "directors_by_year not returning a list" 

    print("All tests passed!")
