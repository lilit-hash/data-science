from unittest.mock import MagicMock, mock_open, patch

import pytest

from movielens_analytics.imdb_parser import FinancialIndicators
from movielens_analytics.links import Links
from movielens_analytics.movies import Movies


class TestLinks:
    """Tests for the Links class."""

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
                3,Grumpier Old Men (1995),Comedy|Romance
                """
            ).strip(),
        ):
            return Movies("dummy_path")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            movieId,imdbId,tmdbId
            1,0114709,862
            2,0113497,8844
            3,0113228,15602
            """
        ).strip(),
    )
    @patch("movielens_analytics.links.ImdbMovie")
    def test_get_imdb(self, mock_imdb_movie: MagicMock, _, movies: Movies):
        """Test the get_imdb method."""
        mock_movie_instance = MagicMock()
        mock_director = MagicMock()
        mock_director.display_name = "John Lasseter"
        mock_movie_instance.directors = [mock_director]

        def get_financial_indicator_side_effect(
            indicator: FinancialIndicators,
        ) -> int | str:
            return {
                FinancialIndicators.PRODUCTION_BUDGET: 30000000,
                FinancialIndicators.WORLDWIDE_GROSS: 373554033,
            }.get(indicator, "Unknown")

        mock_movie_instance.get_financial_indicator.side_effect = (
            get_financial_indicator_side_effect
        )
        mock_movie_instance.runtime = 81
        mock_imdb_movie.return_value = mock_movie_instance

        links = Links("dummy_path", movies)
        expected: list[list[int | str]] = [[1, "John Lasseter", 30000000, 373554033, 81]]
        assert links.get_imdb([1]) == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            movieId,imdbId,tmdbId
            1,0114709,862
            2,0113497,8844
            """
        ).strip(),
    )
    def test_load_links(self, _, movies: Movies):
        """Test the _load_links method."""
        links = Links("dummy_path", movies)
        assert len(links.data) == 2
        assert links.data[1].imdb_id == "0114709"
        assert links.data[1].tmdb_id == "862"

    @patch("builtins.open", new_callable=mock_open, read_data="movieId,imdbId,tmdbId\n")
    def test_top_directors(self, _, movies: Movies):
        """Test the top_directors method."""
        links = Links("dummy_path", movies)
        expected = {"John Lasseter": 1, "Joe Johnston": 1}
        assert links.top_directors(2) == expected

    @patch("builtins.open", new_callable=mock_open, read_data="movieId,imdbId,tmdbId\n")
    def test_most_expensive(self, _, movies: Movies):
        """Test the most_expensive method."""
        links = Links("dummy_path", movies)
        expected = {"Jumanji (1995)": 65000000.0, "Toy Story (1995)": 30000000.0}
        assert links.most_expensive(2) == expected

    @patch("builtins.open", new_callable=mock_open, read_data="movieId,imdbId,tmdbId\n")
    def test_most_profitable(self, _, movies: Movies):
        """Test the most_profitable method."""
        links = Links("dummy_path", movies)
        expected = {
            "Toy Story (1995)": 343554033,
            "Jumanji (1995)": 197797249,
        }
        assert links.most_profitable(2) == expected

    @patch("builtins.open", new_callable=mock_open, read_data="movieId,imdbId,tmdbId\n")
    def test_longest(self, _, movies: Movies):
        """Test the longest method."""
        links = Links("dummy_path", movies)
        expected = {"Jumanji (1995)": 104, "Grumpier Old Men (1995)": 101}
        assert links.longest(2) == expected

    @patch("builtins.open", new_callable=mock_open, read_data="movieId,imdbId,tmdbId\n")
    def test_top_cost_per_minute(self, _, movies: Movies):
        """Test the top_cost_per_minute method."""
        links = Links("dummy_path", movies)
        expected = {"Jumanji (1995)": 625000.0, "Toy Story (1995)": 370370.37}
        assert links.top_cost_per_minute(2) == expected
