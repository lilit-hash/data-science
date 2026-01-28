from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any

import requests
from babel.numbers import format_currency
from requests.exceptions import RequestException, Timeout


class FinancialIndicators(Enum):
    """Class for describing possible financial indicators"""

    PRODUCTION_BUDGET = "productionBudget"
    WORLDWIDE_GROSS = "worldwideGross"
    DOMESTIC_GROSS = "domesticGross"
    OPENING_WEEKEND_GROSS = "openingWeekendGross"


@dataclass
class Image:
    """Class for image characterictics"""

    url: str
    width: int
    height: int


@dataclass
class Date:
    """Date format class"""

    year: int
    month: int
    day: int


@dataclass
class Money:
    """
    The `Money` class is a data class that represents a monetary value
    with an amount and a currency. It also provides a method `format`
    that formats the monetary value as a currency string using
    the `format_currency` function from the `babel.numbers` module.
    """

    amount: str
    currency: str

    def format(self, pattern: str | None = None, locale: str = "en_US") -> str:
        """
        The `format` method is returning a formatted currency string based on the `amount`,
        `currency`, `pattern`, and `locale` parameters provided to the method.
        The formatting is done using the `format_currency` function with the specified parameters.
        """

        return format_currency(
            number=Decimal(self.amount),
            currency=self.currency,
            format=pattern,
            locale=locale,
        )


@dataclass
class Person:  # pylint: disable=too-many-instance-attributes
    """Class for person characterictics"""

    class Role(Enum):
        """Class for describing key persons"""

        DIRECTORS = "directors"
        WRITERS = "writers"
        STARS = "stars"

    id: str
    display_name: str
    alternative_names: list[str]
    primary_image: Image | None
    primary_professions: list[str]
    biography: str
    height: int
    birth_name: str
    birth_date: Date | None
    birth_location: str
    death_date: Date | None
    death_location: str
    death_reason: str


class ImdbMovieFetchError(Exception):
    """Custom exception for movie data fetching errors"""


class ImdbMovie:
    """Class for fetching IMDB movie data by id"""

    def __init__(self, imdb_id: str) -> None:
        self.base_url = "https://api.imdbapi.dev/"
        self.imdb_id = imdb_id
        self.base_data = self._fetch_data()
        self.statistic_data = self._fetch_data(token="/boxOffice")

    def _fetch_data(self, token: str = "") -> dict[str, Any]:
        """Gets full movie data by IMDB ID in a new format"""
        try:
            response = requests.get(
                url=f"{self.base_url}titles/tt{self.imdb_id}{token}",
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except (
            Timeout,
            RequestException,
            ValueError,
            KeyError,
        ) as e:
            raise ImdbMovieFetchError(
                f"Failed to fetch movie data for {self.imdb_id}: {str(e)}"
            ) from e

    @property
    def title(self) -> str:
        """Returns movie title or empty string if no data"""
        return self.base_data.get("primaryTitle", "")

    @property
    def directors(self) -> list[Person]:
        """Returns list of directors"""
        return self.get_persons(Person.Role.DIRECTORS)

    @property
    def writers(self) -> list[Person]:
        """Returns list of writers"""
        return self.get_persons(Person.Role.WRITERS)

    @property
    def stars(self) -> list[Person]:
        """Returns list of stars"""
        return self.get_persons(Person.Role.STARS)

    @property
    def rating(self) -> float:
        """Returns movie rating or 0.0 if no data"""
        rating = 0.0
        if rating_data := self.base_data.get("rating"):
            rating = rating_data.get("aggregateRating", rating)
        return rating

    @property
    def runtime(self) -> int:
        """Returns runtime in seconds or 0 if no data"""
        return self.base_data.get("runtimeSeconds", 0)

    @property
    def image(self) -> Image | None:
        """Returns movie image or None if no data"""
        image = None
        if image_data := self.base_data.get("primaryImage"):
            image = Image(**image_data)
        return image

    @property
    def genres(self) -> list[str]:
        """Returns list of genres"""
        return self.base_data.get("genres", [])

    @property
    def plot(self) -> str:
        """Returns movie plot or empty string"""
        return self.base_data.get("plot", "")

    @property
    def release_year(self) -> int | None:
        """Returns release year or None"""
        return self.base_data.get("startYear")

    def get_financial_indicator(self, indicator: FinancialIndicators, locale: str = "en_US") -> str:
        """Returns financial indicator or empty string"""
        value = "Unknown"

        if indicator_data := self.statistic_data.get(indicator.value, {}):
            money = (
                Money(**indicator_data["gross"])
                if "gross" in indicator_data
                else Money(**indicator_data)
            )
            value = money.format(locale=locale)

        return value

    def get_persons(self, role: Person.Role) -> list[Person]:
        """Returns list of persons for specified role"""
        return self._parse_persons(self.base_data.get(role.value, []))

    @staticmethod
    def _parse_persons(persons_data: list[dict[str, Any]]) -> list[Person]:
        """Parses data about persons (directors, screenwriters, actors)"""
        persons: list[Person] = []

        for person_data in persons_data:
            primary_image = None
            if image_data := person_data.get("primaryImage"):
                primary_image = Image(**image_data)

            birth_date = None
            if birth_date_data := person_data.get("birth_date"):
                birth_date = Date(**birth_date_data)

            death_date = None
            if death_date_data := person_data.get("deathDate"):
                death_date = Date(**death_date_data)

            persons.append(
                Person(
                    id=person_data.get("id", ""),
                    display_name=person_data.get("displayName", ""),
                    alternative_names=person_data.get("alternativeNames", []),
                    primary_image=primary_image,
                    primary_professions=person_data.get("primaryProfessions", []),
                    biography=person_data.get("biography", ""),
                    height=person_data.get("heightCm", 0),
                    birth_name=person_data.get("birthName", ""),
                    birth_date=birth_date,
                    birth_location=person_data.get("birthLocation", ""),
                    death_date=death_date,
                    death_location=person_data.get("deathLocation", ""),
                    death_reason=person_data.get("deathReason", ""),
                )
            )

        return persons
