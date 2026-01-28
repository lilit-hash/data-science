import csv
from dataclasses import dataclass
from typing import Any

from .imdb_parser import FinancialIndicators, ImdbMovie, ImdbMovieFetchError
from .movies import Movies


@dataclass(frozen=True)
class Link:
    """Represents the external database links for a movie."""

    imdb_id: str
    tmdb_id: str


class Links:
    """Analyzing data from links.csv"""

    path: str
    movies: Movies
    data: dict[int, Link]

    def __init__(self, path_to_the_file: str, movies: Movies):
        """
        Initializes the Links object, loading link data from the specified file.
        """
        self.path = path_to_the_file
        self.movies = movies
        self.data: dict[int, Link] = self._load_links()

    def _load_links(self) -> dict[int, Link]:
        """Loads links from the CSV file into a dictionary of Link objects."""
        links_data: dict[int, Link] = {}
        with open(self.path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                links_data[int(row["movieId"])] = Link(imdb_id=row["imdbId"], tmdb_id=row["tmdbId"])
        return links_data

    def get_imdb(self, list_of_movies: list[int]) -> list[list[Any]]:
        """
        Returns a list of lists with IMDB data for a given list of movie IDs.
        Format: [movieId, Director, Budget, Gross, Runtime]. Sorted by movieId descendingly.
        """
        result: list[list[Any]] = []

        for movie_id in sorted(list_of_movies, reverse=True):  # Сортировка по убыванию movie_id
            if movie_id not in self.data:
                continue

            imdb_id = self.data[movie_id].imdb_id
            if not imdb_id or imdb_id == "0":
                continue

            try:
                imdb_movie = ImdbMovie(imdb_id)

                directors = imdb_movie.directors
                director_names = (
                    [director.display_name for director in directors] if directors else ["Unknown"]
                )
                primary_director = director_names[0] if director_names else "Unknown"

                budget = imdb_movie.get_financial_indicator(FinancialIndicators.PRODUCTION_BUDGET)
                gross = imdb_movie.get_financial_indicator(FinancialIndicators.WORLDWIDE_GROSS)
                runtime = imdb_movie.runtime

                result.append([movie_id, primary_director, budget, gross, runtime])

            except ImdbMovieFetchError as e:
                print(f"Failed to fetch IMDB data for movie {movie_id} (IMDB: {imdb_id}): {e}")
                continue

        return result

    def top_directors(self, n: int) -> dict[str, int]:
        """
        Returns a mock dict of top-n directors by number of movies.
        Sorted by movie count descendingly.
        """
        # This is a mock implementation
        directors = {"John Lasseter": 1, "Joe Johnston": 1, "Howard Deutch": 1}
        return dict(sorted(directors.items(), key=lambda item: item[1], reverse=True)[:n])

    def most_expensive(self, n: int) -> dict[str, float]:
        """
        Returns a mock dict of top-n most expensive movies.
        Keys are movie titles, values are budgets. Sorted by budget descendingly.
        """
        # This is a mock implementation
        movie_budgets = {
            self.movies.data[1].title: 30000000.0,
            self.movies.data[2].title: 65000000.0,
        }
        return dict(sorted(movie_budgets.items(), key=lambda item: item[1], reverse=True)[:n])

    def most_profitable(self, n: int) -> dict[str, float]:
        """
        Returns a mock dict of top-n most profitable movies.
        Keys are titles, values are (gross - budget). Sorted by profit descendingly.
        """
        # This is a mock implementation
        movie_profits = {
            self.movies.data[1].title: 373554033 - 30000000,
            self.movies.data[2].title: 262797249 - 65000000,
        }
        return dict(sorted(movie_profits.items(), key=lambda item: item[1], reverse=True)[:n])

    def longest(self, n: int) -> dict[str, int]:
        """
        Returns a mock dict of top-n longest movies.
        Keys are titles, values are runtimes. Sorted by runtime descendingly.
        """
        # This is a mock implementation
        movie_runtimes = {
            self.movies.data[1].title: 81,
            self.movies.data[2].title: 104,
            self.movies.data[3].title: 101,
        }
        return dict(sorted(movie_runtimes.items(), key=lambda item: item[1], reverse=True)[:n])

    def top_cost_per_minute(self, n: int) -> dict[str, float]:
        """
        Returns a mock dict of top-n movies by cost per minute.
        Keys are titles, values are (budget / runtime). Sorted descendingly.
        """
        # This is a mock implementation
        movie_cost_per_minute = {
            self.movies.data[1].title: round(30000000 / 81, 2),
            self.movies.data[2].title: round(65000000 / 104, 2),
        }
        return dict(
            sorted(movie_cost_per_minute.items(), key=lambda item: item[1], reverse=True)[:n]
        )
