from unittest.mock import mock_open, patch

import pytest

from movielens_analytics.movies import Movies
from movielens_analytics.ratings import Ratings
from movielens_analytics.users import Users


class TestUsers:
    """Tests for the Users class."""

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

    @pytest.fixture
    def ratings(self, movies: Movies) -> Ratings:
        """Fixture for a Ratings object."""
        with patch(
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
        ):
            return Ratings("dummy_path", movies)

    def test_dist_by_num_of_ratings(self, ratings: Ratings):
        """Test the dist_by_num_of_ratings method."""
        users = Users(ratings)
        expected = {1: 2, 2: 2}
        assert users.dist_by_num_of_ratings() == expected

    def test_dist_by_rating_metric(self, ratings: Ratings):
        """Test the dist_by_rating_metric method."""
        users = Users(ratings)
        expected = {1: 4.0, 2: 4.5}
        assert users.dist_by_rating_metric() == expected

    def test_top_by_variance(self, ratings: Ratings):
        """Test the top_by_variance method."""
        users = Users(ratings)
        expected = {2: 0.5, 1: 0.0}
        assert users.top_by_variance(2) == expected

    def test_dist_by_rating_metric_median(self, ratings: Ratings):
        """Test the dist_by_rating_metric method with median metric."""
        users = Users(ratings)
        expected = {1: 4.0, 2: 4.5}
        assert users.dist_by_rating_metric(metric="median") == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,rating,timestamp
            1,1,1.0,964982703
            1,2,5.0,964982703
            2,1,4.0,964982703
            """
        ).strip(),
    )
    def test_top_by_variance_single_rating(self, _, movies: Movies):
        """Test the top_by_variance method with a user having a single rating."""
        ratings = Ratings("dummy_path", movies)
        users = Users(ratings)
        expected = {1: 8.0}
        assert users.top_by_variance(1) == expected
