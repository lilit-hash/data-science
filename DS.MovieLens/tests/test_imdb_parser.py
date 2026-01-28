"""Unit tests for the imdb_parser module."""

from typing import Any
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError, RequestException, Timeout

from movielens_analytics.imdb_parser import (
    FinancialIndicators,
    ImdbMovie,
    ImdbMovieFetchError,
    Money,
    Person,
)

TEST_IMDB_ID = 114709
MOCK_BASE_DATA: dict[str, Any] = {
    "id": "tt0114709",
    "type": "movie",
    "primaryTitle": "Toy Story",
    "primaryImage": {
        "url": (
            "https://m.media-amazon.com/images/M/"
            "MV5BZTA3OWVjOWItNjE1NS00NzZiLWE1MjgtZDZhMWI1ZTlkNzYwXkEyXkFqcGc@._V1_.jpg"
        ),
        "width": 1005,
        "height": 1500,
    },
    "startYear": 1995,
    "runtimeSeconds": 4860,
    "genres": ["Animation", "Adventure", "Comedy", "Family", "Fantasy"],
    "rating": {"aggregateRating": 8.3, "voteCount": 1146830},
    "metacritic": {"score": 96, "reviewCount": 26},
    "plot": "A cowboy doll is profoundly jealous...",
    "directors": [
        {
            "id": "nm0005124",
            "displayName": "John Lasseter",
            "alternativeNames": ["Lasseter"],
            "primaryImage": {
                "url": (
                    "https://m.media-amazon.com/images/M/"
                    "MV5BMTQ5NTczNjE5MV5BMl5BanBnXkFtZTcwMTA1MTQ3Mg@@._V1_.jpg"
                ),
                "width": 312,
                "height": 400,
            },
            "primaryProfessions": ["miscellaneous", "producer", "writer"],
        }
    ],
    "writers": [
        {
            "id": "nm0005124",
            "displayName": "John Lasseter",
            "alternativeNames": ["Lasseter"],
            "primaryImage": {
                "url": (
                    "https://m.media-amazon.com/images/M/"
                    "MV5BMTQ5NTczNjE5MV5BMl5BanBnXkFtZTcwMTA1MTQ3Mg@@._V1_.jpg"
                ),
                "width": 312,
                "height": 400,
            },
            "primaryProfessions": ["miscellaneous", "producer", "writer"],
        },
        {
            "id": "nm0230032",
            "displayName": "Pete Docter",
            "alternativeNames": ["Peter Docter", "Pete Doctor"],
            "primaryImage": {
                "url": (
                    "https://m.media-amazon.com/images/M/"
                    "MV5BZjg1OWQxM2MtMjY4Yi00OTA4LTlhMmYtMDgwOTJjYjVlZDgxXkEyXkFqcGc@._V1_.jpg"
                ),
                "width": 3299,
                "height": 5000,
            },
            "primaryProfessions": ["miscellaneous", "producer", "writer"],
        },
        {
            "id": "nm0004056",
            "displayName": "Andrew Stanton",
            "alternativeNames": [
                "Andy",
                'Andrew "Boog" Stanton',
                "Andrew A. Stanton",
                "Andy Stanton",
            ],
            "primaryImage": {
                "url": (
                    "https://m.media-amazon.com/images/M/"
                    "MV5BMmZiOTE4NDktMmZjNi00MzcwLWJjMzAtYWVlZDUwNjhiMGIwXkEyXkFqcGc@._V1_.jpg"
                ),
                "width": 750,
                "height": 1044,
            },
            "primaryProfessions": ["actor", "producer", "writer"],
        },
    ],
    "stars": [
        {
            "id": "nm0000158",
            "displayName": "Tom Hanks",
            "alternativeNames": ["Tom H.", "Tomu Hankusu"],
            "primaryImage": {
                "url": (
                    "https://m.media-amazon.com/images/M/"
                    "MV5BMTQ2MjMwNDA3Nl5BMl5BanBnXkFtZTcwMTA2NDY3NQ@@._V1_.jpg"
                ),
                "width": 1417,
                "height": 2048,
            },
            "primaryProfessions": ["actor", "producer", "writer"],
        },
    ],
    "originCountries": [{"code": "US", "name": "United States"}],
    "spokenLanguages": [{"code": "eng", "name": "English"}],
    "interests": [
        {"id": "in0000012", "name": "Adventure"},
        {"id": "in0000024", "name": "Urban Adventure", "isSubgenre": True},
        {"id": "in0000026", "name": "Animation"},
        {"id": "in0000028", "name": "Computer Animation"},
        {"id": "in0000032", "name": "Buddy Comedy", "isSubgenre": True},
        {"id": "in0000034", "name": "Comedy"},
        {"id": "in0000093", "name": "Family"},
        {"id": "in0000098", "name": "Fantasy"},
        {"id": "in0000099", "name": "Supernatural Fantasy", "isSubgenre": True},
    ],
}

MOCK_STATISTIC_DATA: dict[str, Any] = {
    "domesticGross": {"amount": "229947062", "currency": "USD"},
    "worldwideGross": {"amount": "401157969", "currency": "USD"},
    "openingWeekendGross": {
        "gross": {"amount": "29140617", "currency": "USD"},
        "weekendEndDate": {"year": 1995, "month": 11, "day": 26},
    },
    "productionBudget": {"amount": "30000000", "currency": "USD"},
}


@pytest.fixture
def mock_requests_get():
    """Fixture to mock requests.get with side effects for different URLs."""
    with patch("requests.get") as mock_get:
        # Define a side effect function to return different mocks based on URL
        def side_effect(url: str, **_):
            mock_response = Mock()
            if "/boxOffice" in url:
                mock_response.json.return_value = MOCK_STATISTIC_DATA
                mock_response.status_code = 200
            elif f"tt{TEST_IMDB_ID}" in url:
                mock_response.json.return_value = MOCK_BASE_DATA
                mock_response.status_code = 200
            else:
                mock_response.status_code = 404
                mock_response.reason = "Not Found"
                mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
            return mock_response

        mock_get.side_effect = side_effect
        yield mock_get


class TestImdbMovie:
    """Tests for the ImdbMovie class."""

    @pytest.fixture
    def movie_instance(self, mock_requests_get: Mock) -> ImdbMovie:  # pylint: disable=redefined-outer-name, unused-argument
        """Fixture for a fully mocked ImdbMovie object."""
        return ImdbMovie(str(TEST_IMDB_ID))

    def test_init(self, movie_instance: ImdbMovie, mock_requests_get: Mock):  # pylint: disable=redefined-outer-name
        """Test that __init__ fetches data correctly."""
        assert movie_instance.imdb_id == str(TEST_IMDB_ID)
        assert movie_instance.base_data == MOCK_BASE_DATA
        assert movie_instance.statistic_data == MOCK_STATISTIC_DATA
        assert mock_requests_get.call_count == 2

    def test_title_property(self, movie_instance: ImdbMovie):
        """Test the title property."""
        assert movie_instance.title == "Toy Story"

    def test_release_year_property(self, movie_instance: ImdbMovie):
        """Test the release_year property."""
        assert movie_instance.release_year == 1995

    def test_runtime_property(self, movie_instance: ImdbMovie):
        """Test the runtime property."""
        assert movie_instance.runtime == 4860

    def test_genres_property(self, movie_instance: ImdbMovie):
        """Test the genres property."""
        assert movie_instance.genres == ["Animation", "Adventure", "Comedy", "Family", "Fantasy"]

    def test_plot_property(self, movie_instance: ImdbMovie):
        """Test the plot property."""
        assert movie_instance.plot == "A cowboy doll is profoundly jealous..."

    def test_rating_property(self, movie_instance: ImdbMovie):
        """Test the rating property."""
        assert movie_instance.rating == 8.3

    def test_image_property(self, movie_instance: ImdbMovie):
        """Test the image property."""
        image = movie_instance.image
        assert image is not None
        assert image.url == (
            "https://m.media-amazon.com/images/M/"
            "MV5BZTA3OWVjOWItNjE1NS00NzZiLWE1MjgtZDZhMWI1ZTlkNzYwXkEyXkFqcGc@._V1_.jpg"
        )
        assert image.width == 1005

    def test_directors_property(self, movie_instance: ImdbMovie):
        """Test the directors property."""
        directors = movie_instance.directors
        assert len(directors) == 1
        assert isinstance(directors[0], Person)
        assert directors[0].display_name == "John Lasseter"

    def test_stars_property(self, movie_instance: ImdbMovie):
        """Test the stars property."""
        stars = movie_instance.stars
        assert len(stars) == 1
        assert stars[0].display_name == "Tom Hanks"

    def test_get_financial_indicator(self, movie_instance: ImdbMovie):
        """Test the get_financial_indicator method."""
        budget = movie_instance.get_financial_indicator(
            FinancialIndicators.PRODUCTION_BUDGET, locale="en_US"
        )
        # Using non-breaking space as per babel's default
        assert budget.replace("\u202f", " ") == "$30,000,000.00"

        gross = movie_instance.get_financial_indicator(
            FinancialIndicators.WORLDWIDE_GROSS, locale="ru_RU"
        )
        assert gross.replace("\u202f", " ").replace("\xa0", " ") == "401 157 969,00 $"

    def test_get_financial_indicator_unknown(self, movie_instance: ImdbMovie):
        """Test get_financial_indicator for a missing indicator."""
        value = movie_instance.get_financial_indicator(FinancialIndicators.OPENING_WEEKEND_GROSS)
        assert value == "$29,140,617.00"

    @patch("requests.get")
    def test_fetch_data_raises_on_timeout(self, mock_get: Mock):
        """Test that _fetch_data raises ImdbMovieFetchError on Timeout."""
        mock_get.side_effect = Timeout("Connection timed out")
        with pytest.raises(ImdbMovieFetchError, match="timed out"):
            ImdbMovie(str(TEST_IMDB_ID))

    @patch("requests.get")
    def test_fetch_data_raises_on_request_exception(self, mock_get: Mock):
        """Test that _fetch_data raises ImdbMovieFetchError on RequestException."""
        mock_get.side_effect = RequestException("Network error")
        with pytest.raises(ImdbMovieFetchError, match="Network error"):
            ImdbMovie(str(TEST_IMDB_ID))

    @patch("requests.get")
    def test_fetch_data_raises_on_http_error(self, mock_get: Mock):
        """Test that _fetch_data raises ImdbMovieFetchError on HTTPError."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
        mock_get.return_value = mock_response
        with pytest.raises(ImdbMovieFetchError, match="404 Client Error"):
            ImdbMovie(str(TEST_IMDB_ID))


class TestMoney:
    """Tests for the Money dataclass."""

    def test_format(self):
        """Test the format method of the Money class."""
        money = Money(amount="12345.67", currency="USD")
        assert money.format(locale="en_US") == "$12,345.67"
        assert money.format(locale="ru_RU") == "12\xa0345,67\xa0$"
        assert money.format(pattern="¤###0", locale="en_US") == "$12345.67"
