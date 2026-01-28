import csv
import re
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    """Represents a single movie."""

    movie_id: int
    title: str
    genres: list[str]


class Movies:
    """Analyzing data from movies.csv"""

    path: str
    data: dict[int, Movie]

    def __init__(self, path_to_the_file: str):
        """
        Initializes the Movies object, loading movie data from the specified file.
        """
        self.path = path_to_the_file
        self.data: dict[int, Movie] = self._load_movies()

    def _load_movies(self) -> dict[int, Movie]:
        """
        Loads movies from the CSV file into a dictionary of Movie objects.
        """
        movies_data: dict[int, Movie] = {}
        with open(self.path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                movie_id = int(row["movieId"])
                movies_data[movie_id] = Movie(
                    movie_id=movie_id,
                    title=row["title"],
                    genres=row["genres"].split("|"),
                )
        return movies_data

    def dist_by_release(self) -> dict[int, int]:
        """
        Calculates the distribution of movies by their release year.
        Returns a dict where keys are years and values are movie counts,
        sorted by count descendingly.
        """
        years: list[int] = []
        for movie in self.data.values():
            match = re.search(r"\((\d{4})\)", movie.title)
            if match:
                years.append(int(match.group(1)))
        year_counts = Counter(years)
        return dict(sorted(year_counts.items(), key=lambda item: item[1], reverse=True))

    def dist_by_genres(self) -> dict[str, int]:
        """
        Calculates the distribution of movies by genre.
        Returns a dict where keys are genres and values are counts,
        sorted by count descendingly.
        """
        genres: list[str] = [genre for movie in self.data.values() for genre in movie.genres]
        genre_counts = Counter(genres)
        return dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True))

    def most_genres(self, n: int) -> dict[str, int]:
        """
        Finds the top-n movies with the most genres.
        Returns a dict where keys are movie titles and values are the number of genres,
        sorted by count descendingly.
        """
        movie_genres_count: dict[str, int] = {
            movie.title: len(movie.genres) for movie in self.data.values()
        }
        sorted_movies = sorted(movie_genres_count.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_movies[:n])
