from unittest.mock import mock_open, patch

import pytest

from movielens_analytics.movies import Movies
from movielens_analytics.ratings import Ratings


class TestRatings:
    """Tests for the Ratings class."""

    @pytest.fixture
    def movies(self) -> Movies:
        """Fixture for a Movies object."""
        with patch(
            "builtins.open",
            new_callable=mock_open,
            read_data=(
                """
                movieId,title,genres
                1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
                2,Jumanji (1995),Adventure|Children|Fantasy
                """
            ).strip(),
        ):
            return Movies("dummy_path")

    def test_ratings_initialization(self, movies: Movies):
        """Test the __init__ method of the Ratings class."""
        with patch(
            "builtins.open",
            new_callable=mock_open,
            read_data=(
                """
                userId,movieId,rating,timestamp
                1,1,4.0,964982703
                1,2,4.0,964982703
                """
            ).strip(),
        ):
            ratings = Ratings("dummy_path", movies)
            assert ratings.path == "dummy_path"
            assert ratings.movies == movies
            assert len(ratings.data) == 2

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,rating,timestamp
            1,1,4.0,964982703
            1,2,4.0,964982703
            2,1,4.0,964982703
            2,2,5.0,964982703
            """
        ).strip(),
    )
    def test_dist_by_year(self, _, movies: Movies):
        """Test the dist_by_year method."""
        ratings = Ratings("dummy_path", movies)
        expected = {2000: 4}
        assert ratings.dist_by_year() == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,rating,timestamp
            1,1,4.0,964982703
            1,2,4.0,964982703
            2,1,4.0,964982703
            2,2,5.0,964982703
            """
        ).strip(),
    )
    def test_dist_by_rating(self, _, movies: Movies):
        """Test the dist_by_rating method."""
        ratings = Ratings("dummy_path", movies)
        expected = {4.0: 3, 5.0: 1}
        assert ratings.dist_by_rating() == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,rating,timestamp
            1,1,4.0,964982703
            1,2,4.0,964982703
            2,1,4.0,964982703
            2,2,5.0,964982703
            """
        ).strip(),
    )
    def test_top_by_num_of_ratings(self, _, movies: Movies):
        """Test the top_by_num_of_ratings method."""
        ratings = Ratings("dummy_path", movies)
        expected = {"Toy Story (1995)": 2, "Jumanji (1995)": 2}
        assert ratings.top_by_num_of_ratings(2) == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,rating,timestamp
            1,1,1.0,964982703
            2,1,5.0,964982703
            1,2,2.0,964982703
            2,2,4.0,964982703
            """
        ).strip(),
    )
    def test_top_by_ratings_average(self, _, movies: Movies):
        """Test the top_by_ratings method with average metric."""
        ratings = Ratings("dummy_path", movies)
        expected = {"Jumanji (1995)": 0.06, "Toy Story (1995)": 0.06}
        assert ratings.top_by_ratings(2, metric="average") == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,rating,timestamp
            1,1,1.0,964982703
            2,1,5.0,964982703
            3,1,3.0,964982703
            1,2,2.0,964982703
            2,2,4.0,964982703
            """
        ).strip(),
    )
    def test_top_by_ratings_median(self, _, movies: Movies):
        """Test the top_by_ratings method with median metric."""
        ratings = Ratings("dummy_path", movies)
        expected = {"Toy Story (1995)": 0.09, "Jumanji (1995)": 0.06}
        assert ratings.top_by_ratings(2, metric="median") == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,rating,timestamp
            1,1,1.0,964982703
            2,1,5.0,964982703
            1,2,3.0,964982703
            2,2,3.0,964982703
            """
        ).strip(),
    )
    def test_top_controversial(self, _, movies: Movies):
        """Test the top_controversial method."""
        ratings = Ratings("dummy_path", movies)
        expected = {"Toy Story (1995)": 8.0}
        assert ratings.top_controversial(1) == expected
