import csv
import statistics
from collections import Counter
from dataclasses import dataclass
from datetime import datetime

from .movies import Movies


@dataclass(frozen=True)
class Rating:
    """Represents a single rating."""

    user_id: int
    movie_id: int
    rating: float
    timestamp: datetime


class Ratings:
    """Analyzing data from ratings.csv"""

    path: str
    movies: Movies
    data: list[Rating]

    def __init__(self, path_to_the_file: str, movies: Movies):
        """
        Initializes the Ratings object, loading ratings data from the specified file.
        """
        self.path = path_to_the_file
        self.movies = movies
        self.data: list[Rating] = self._load_ratings()

    def _load_ratings(self) -> list[Rating]:
        """Loads ratings from the CSV file into a list of Rating objects."""
        ratings_data: list[Rating] = []
        with open(self.path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ratings_data.append(
                    Rating(
                        user_id=int(row["userId"]),
                        movie_id=int(row["movieId"]),
                        rating=float(row["rating"]),
                        timestamp=datetime.fromtimestamp(int(row["timestamp"])),
                    )
                )
        return ratings_data

    def dist_by_year(self) -> dict[int, int]:
        """
        Calculates the distribution of ratings by year.
        Returns a dict where keys are years and values are counts,
        sorted by year ascendingly.
        """
        years = [rating.timestamp.year for rating in self.data]
        year_counts = Counter(years)
        return dict(sorted(year_counts.items()))

    def dist_by_rating(self) -> dict[float, int]:
        """
        Calculates the distribution of ratings by rating value.
        Returns a dict where keys are ratings and values are counts,
        sorted by rating ascendingly.
        """
        ratings_values = [rating.rating for rating in self.data]
        rating_counts = Counter(ratings_values)
        return dict(sorted(rating_counts.items()))

    def top_by_num_of_ratings(self, n: int) -> dict[str, int]:
        """
        Finds the top-n movies by the number of ratings.
        Returns a dict where keys are movie titles and values are the rating counts,
        sorted descendingly.
        """

        n = max(n, 0)

        # if n < 0:
        #     n = 0
        #     raise ValueError(f"Parameter n must be non-negative, got {n}")

        movie_ratings = [rating.movie_id for rating in self.data]
        movie_counts = Counter(movie_ratings)
        sorted_movies = sorted(movie_counts.items(), key=lambda item: item[1], reverse=True)
        top_movies: dict[str, int] = {}
        for movie_id, count in sorted_movies[:n]:
            if movie_id in self.movies.data:
                top_movies[self.movies.data[movie_id].title] = count
        return top_movies

    def top_by_ratings(
        self, n: int, metric: str = "average", min_ratings: int = 100
    ) -> dict[str, float]:
        """
        Finds the top-n movies by average or median rating.
        Returns a dict where keys are movie titles and values are the metric,
        sorted descendingly. Values are rounded to 2 decimal places.
        """
        movie_ratings: dict[int, list[float]] = {}
        for rating in self.data:
            movie_ratings.setdefault(rating.movie_id, []).append(rating.rating)

        movie_metrics: dict[int, float] = {}
        for movie_id, ratings_list in movie_ratings.items():
            if not ratings_list:
                continue
            num_ratings = len(ratings_list)
            weight = min(num_ratings / min_ratings, 1.0)
            if metric == "average":
                movie_metrics[movie_id] = round(statistics.mean(ratings_list), 2) * weight
            elif metric == "median":
                movie_metrics[movie_id] = round(statistics.median(ratings_list), 2) * weight

        sorted_movies: list[tuple[int, float]] = sorted(
            movie_metrics.items(), key=lambda item: item[1], reverse=True
        )
        top_movies: dict[str, float] = {}
        for movie_id, metric_value in sorted_movies[:n]:
            if movie_id in self.movies.data:
                top_movies[self.movies.data[movie_id].title] = metric_value
        return top_movies

    def top_controversial(self, n: int) -> dict[str, float]:
        """
        Finds the top-n most controversial movies by rating variance.
        Returns a dict where keys are movie titles and values are the variance,
        sorted descendingly. Values are rounded to 2 decimal places.
        """
        movie_ratings: dict[int, list[float]] = {}
        for rating in self.data:
            movie_ratings.setdefault(rating.movie_id, []).append(rating.rating)

        movie_variances: dict[int, float] = {}
        for movie_id, ratings_list in movie_ratings.items():
            if len(ratings_list) > 1:
                movie_variances[movie_id] = round(statistics.variance(ratings_list), 2)

        sorted_movies: list[tuple[int, float]] = sorted(
            movie_variances.items(), key=lambda item: item[1], reverse=True
        )
        top_movies: dict[str, float] = {}
        for movie_id, variance in sorted_movies[:n]:
            if movie_id in self.movies.data:
                top_movies[self.movies.data[movie_id].title] = variance
        return top_movies
