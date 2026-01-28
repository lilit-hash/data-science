"""Integration tests module"""

import os
from datetime import datetime

import pytest

from movielens_analytics.links import Links
from movielens_analytics.movies import Movies
from movielens_analytics.ratings import Ratings
from movielens_analytics.tags import Tags

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "datasets"))
MOVIES_FILE = os.path.join(DATA_DIR, "movies.csv")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.csv")
LINKS_FILE = os.path.join(DATA_DIR, "links.csv")
TAGS_FILE = os.path.join(DATA_DIR, "tags.csv")


@pytest.mark.skipif(not os.path.exists(MOVIES_FILE), reason="Data files not found")
class TestMoviesIntegration:
    """Integration tests for the Movies class using real data."""

    @pytest.fixture(scope="class")
    def movies_instance(self):
        """Fixture to create a Movies instance for integration tests."""
        return Movies(MOVIES_FILE)

    @pytest.fixture(scope="class")
    def links_instance(self, movies_instance: Movies):
        """Fixture to create a Links instance for integration tests."""
        return Links(LINKS_FILE, movies=movies_instance)

    def test_init_loads_movies_correctly_integration(self, movies_instance: Movies):
        """Test that Movies class initializes correctly with the real movies.csv."""
        # There are 9742 movies in the dataset.
        assert len(movies_instance.data) == 9742
        # Check the first movie
        assert movies_instance.data[1].title == "Toy Story (1995)"
        assert movies_instance.data[1].genres == [
            "Adventure",
            "Animation",
            "Children",
            "Comedy",
            "Fantasy",
        ]
        # Check a movie from the middle
        assert movies_instance.data[2659].title == "It Came from Hollywood (1982)"
        assert movies_instance.data[2659].genres == ["Comedy", "Documentary"]

    def test_dist_by_release_integration(self, movies_instance: Movies):
        """Test dist_by_release with real data."""
        release_dist = movies_instance.dist_by_release()
        # Check a few years for which we can be reasonably sure of the data
        assert release_dist[1995] == 259
        assert release_dist[2000] == 283
        assert release_dist[2017] == 147
        assert release_dist.get(1902, 0) >= 1

    def test_dist_by_genres_integration(self, movies_instance: Movies):
        """Test dist_by_genres with real data."""
        genre_dist = movies_instance.dist_by_genres()
        assert genre_dist["Drama"] > 4000
        assert genre_dist["Comedy"] > 3500
        assert genre_dist["Action"] > 1800
        assert genre_dist["(no genres listed)"] >= 34

    def test_most_genres_integration(self, movies_instance: Movies):
        """Test most_genres with real data."""
        top_5 = movies_instance.most_genres(5)
        assert len(top_5) == 5

        # Verify that the genre counts for the returned movies are correct
        for title, count in top_5.items():
            # Find the movie in the full dataset
            found_movie = None
            for movie in movies_instance.data.values():
                if movie.title == title:
                    found_movie = movie
                    break
            assert found_movie is not None
            assert len(found_movie.genres) == count
            # Assuming top movies have at least 8 genres
            assert count >= 7


@pytest.mark.skipif(not os.path.exists(MOVIES_FILE), reason="Data files not found")
@pytest.mark.skipif(not os.path.exists(RATINGS_FILE), reason="Data files not found")
class TestRatingsIntegration:
    """Integration tests for the Ratings class using real data."""

    @pytest.fixture(scope="class")
    def movies_instance(self):
        """Fixture to create a Movies instance for integration tests."""
        return Movies(MOVIES_FILE)

    @pytest.fixture(scope="class")
    def ratings_instance(self, movies_instance: Movies):
        """Fixture to create a Ratings instance for integration tests."""
        return Ratings(RATINGS_FILE, movies=movies_instance)

    def test_init_load_ratings_correctly_integration(self, ratings_instance: Ratings):
        """Test that Ratings class initializes correctly with the real ratings.csv."""

        # Check specific ratings data
        assert len(ratings_instance.data) == 100836
        assert ratings_instance.data[10].movie_id == 163
        assert ratings_instance.data[1].user_id == 1
        assert ratings_instance.data[20].rating == 4.0

        timestamp_value = ratings_instance.data[47324].timestamp
        expected_datetime = expected_datetime = datetime.fromtimestamp(1190852080)
        assert timestamp_value == expected_datetime

    def test_dist_by_year_integration(self, ratings_instance: Ratings):
        """Test dist_by_year method with real data."""
        year_distribution = ratings_instance.dist_by_year()

        # Check that the result is a dictionary
        assert isinstance(year_distribution, dict)

        # Check that the years are sorted in ascending order
        years = list(year_distribution.keys())
        assert years == sorted(years)

        assert year_distribution[2000] >= 5000
        assert year_distribution[2005] >= 5000
        assert year_distribution[2015] >= 5000

        # Check that the sum of all ratings is equal to the total number
        total_ratings = sum(year_distribution.values())
        assert total_ratings == 100836

    def test_dist_by_rating_integration(self, ratings_instance: Ratings):
        """Test dist_by_rating method with real data."""
        rating_distribution = ratings_instance.dist_by_rating()

        # Check that the result is a dictionary
        assert isinstance(rating_distribution, dict)

        # Check that the years are sorted in ascending order
        ratings = list(rating_distribution.keys())
        assert ratings == sorted(ratings)

        expected_ratings = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        for expected_rating in expected_ratings:
            assert expected_rating in rating_distribution

        # Check that the sum of all ratings is equal to the total number
        total_ratings = sum(rating_distribution.values())
        assert total_ratings == 100836

        # Check that the distribution has the expected shape
        # (usually more high scores)
        assert rating_distribution[5.0] > rating_distribution[1.0]
        assert rating_distribution[4.0] > rating_distribution[2.0]

    def test_top_by_num_of_ratings_integration(self, ratings_instance: Ratings):
        """Test top_by_num_of_ratings method with real data."""

        top_5 = ratings_instance.top_by_num_of_ratings(5)

        # Check that the result is a dictionary
        assert isinstance(top_5, dict)

        # Check that exactly 5 elements were returned
        assert len(top_5) == 5

        # Check that the values are sorted in descending order of the numder of ratings
        counts = list(top_5.values())
        assert counts == sorted(counts, reverse=True)

        # Check that the keys are movie titles
        for title in top_5.keys():
            assert isinstance(title, str)
            assert len(title) > 0

        # Testing with a different value of n
        top_10 = ratings_instance.top_by_num_of_ratings(10)
        assert len(top_10) == 10

        # We check that the most popular films have a lot of ratings
        top_counts = list(top_5.values())
        assert all(count >= 100 for count in top_counts)

    def test_top_by_ratings_integration(self, ratings_instance: Ratings):
        """Test top_by_ratings method with real data."""

        top_5_avg = ratings_instance.top_by_ratings(5, "average")

        # Check that the result is a dictionary
        assert isinstance(top_5_avg, dict)
        assert len(top_5_avg) == 5

        # Check that the values are sorted in descending order of rating
        ratings_avg = list(top_5_avg.values())
        assert ratings_avg == sorted(ratings_avg, reverse=True)

        # Check that the ratings are within the acceptable range
        for rating in ratings_avg:
            assert 0.0 <= rating <= 5.0
            assert rating == round(rating, 2)

        # Testing the median rating
        top_5_median = ratings_instance.top_by_ratings(5, "median")
        assert isinstance(top_5_median, dict)
        assert len(top_5_median) == 5

        # We check that the medians are also within the acceptable range
        ratings_median = list(top_5_median.values())
        for rating in ratings_median:
            assert 0.0 <= rating <= 5.0
            assert rating == round(rating, 2)

        assert top_5_avg != top_5_median

    def test_top_controversial_integration(self, ratings_instance: Ratings):
        """Test top_controversial method with real data."""

        top_5_controversial = ratings_instance.top_controversial(5)

        # Check that the result is a dictionary
        assert isinstance(top_5_controversial, dict)
        assert len(top_5_controversial) == 5

        # Check that the values are sorted in descending order
        variances = list(top_5_controversial.values())
        assert variances == sorted(variances, reverse=True)

        # Check that the variances are non-negative and rounded
        for variance in variances:
            assert variance >= 0.0
            assert variance == round(variance, 2)

        # Check that the keys are movie titles
        for title in top_5_controversial.keys():
            assert isinstance(title, str)
            assert len(title) > 0

        # Testing with a different value of n
        top_10_controversial = ratings_instance.top_controversial(10)
        assert len(top_10_controversial) == 10

    def test_edge_cases_ratings_methods(self, ratings_instance: Ratings):
        """Test edge cases for Ratings methods."""

        # Testing the boundary values for n
        top_0 = ratings_instance.top_by_num_of_ratings(0)
        assert top_0 == {}

        top_1 = ratings_instance.top_by_num_of_ratings(1)
        assert len(top_1) == 1

        # Testing large n (more than there are movies)
        large_n = ratings_instance.top_by_num_of_ratings(100000)
        assert len(large_n) <= 100836  # Не больше чем общее количество оценок

        # Test for negative n (should return an empty dictionary)
        top_negative = ratings_instance.top_by_num_of_ratings(-1)
        assert top_negative == {}

    def test_rating_statistics_consistency(self, ratings_instance: Ratings):
        """Test that different methods provide consistent results."""

        top_by_count = ratings_instance.top_by_num_of_ratings(10)

        top_by_avg = ratings_instance.top_by_ratings(10, "average")

        # Check for some overlap
        # (usually movies with a lot of ratings also have high ratings)
        common_movies = set(top_by_count.keys()) & set(top_by_avg.keys())
        assert len(common_movies) > 0

        # We check that controversial films do not coincide with the top ones by average rating
        controversial = ratings_instance.top_controversial(10)
        controversial_and_top_avg = set(controversial.keys()) & set(top_by_avg.keys())
        assert len(controversial_and_top_avg) < 5

    def test_rating_data_quality(self, ratings_instance: Ratings):
        """Test the quality and validity of rating data."""

        # Check that all ratings are within the acceptable range
        for rating in ratings_instance.data:
            assert 0.5 <= rating.rating <= 5.0
            assert rating.rating * 2 == int(rating.rating * 2)  # Рейтинги с шагом 0.5

        # Check that all timestamps are in the correct range
        for rating in ratings_instance.data:
            assert rating.timestamp.year >= 1995
            assert rating.timestamp.year <= 2020

        # Check that user_id and movie_id are positive
        for rating in ratings_instance.data:
            assert rating.user_id > 0
            assert rating.movie_id > 0


@pytest.mark.skipif(not os.path.exists(TAGS_FILE), reason="Data files not found")
class TestTagsIntegration:
    """Integration tests for the Tags class using real data."""

    @pytest.fixture(scope="class")
    def tags_instance(self):
        """Fixture to create a Movies instance for integration tests."""
        return Tags(TAGS_FILE)

    def test_tags_init_loads_correctly_integration(self, tags_instance: Tags):
        """Test that Tags class initializes correctly with the real tags.csv."""
        assert len(tags_instance.data) == 3683  # Total tags in the dataset

        # Check specific tag data
        assert tags_instance.data[0].user_id == 2
        assert tags_instance.data[0].movie_id == 60756
        assert tags_instance.data[0].tag == "funny"

        # Check timestamp conversion
        assert tags_instance.data[10].timestamp.year >= 2006
        assert tags_instance.data[10].timestamp.year <= 2018

    def test_most_words_integration(self, tags_instance: Tags):
        """Test most_words method with real data."""
        top_10_most_words = tags_instance.most_words(10)

        assert isinstance(top_10_most_words, dict)
        assert len(top_10_most_words) == 10

        # Check that values are sorted descending by word count
        word_counts = list(top_10_most_words.values())
        assert word_counts == sorted(word_counts, reverse=True)

        # Verify word count calculation
        for tag, count in top_10_most_words.items():
            expected_count = len(tag.split())
            assert count == expected_count
            assert count >= 1  # All tags should have at least 1 word

    def test_longest_integration(self, tags_instance: Tags):
        """Test longest method with real data."""
        top_10_longest = tags_instance.longest(10)

        assert isinstance(top_10_longest, list)
        assert len(top_10_longest) == 10

        # Check that tags are sorted by length descending
        lengths = [len(tag) for tag in top_10_longest]
        assert lengths == sorted(lengths, reverse=True)

        # Check uniqueness
        assert len(top_10_longest) == len(set(top_10_longest))

        # Verify all tags are strings and have reasonable length
        for tag in top_10_longest:
            assert isinstance(tag, str)
            assert len(tag) >= 10  # Longest tags should be reasonably long

    def test_most_words_and_longest_integration(self, tags_instance: Tags):
        """Test most_words_and_longest method with real data."""
        intersection = tags_instance.most_words_and_longest(10)

        assert isinstance(intersection, list)

        # The intersection should be a subset of both
        most_words_tags = set(tags_instance.most_words(10).keys())
        longest_tags = set(tags_instance.longest(10))

        assert set(intersection).issubset(most_words_tags)
        assert set(intersection).issubset(longest_tags)

        # Check that tags in intersection have both many words and are long
        for tag in intersection:
            word_count = len(tag.split())
            tag_length = len(tag)
            assert word_count >= 3  # Should have multiple words
            assert tag_length >= 15  # Should be reasonably long

    def test_most_popular_integration(self, tags_instance: Tags):
        """Test most_popular method with real data."""
        top_10_popular = tags_instance.most_popular(10)

        assert isinstance(top_10_popular, dict)
        assert len(top_10_popular) == 10

        # Check that values are sorted descending by frequency
        frequencies = list(top_10_popular.values())
        assert frequencies == sorted(frequencies, reverse=True)

        # Check specific popular tags that should exist
        common_tags = ["sci-fi", "comedy", "action", "funny", "romance"]
        found_common = any(tag in top_10_popular for tag in common_tags)
        assert found_common  # At least one common tag should be in top

    def test_tags_with_integration(self, tags_instance: Tags):
        """Test tags_with method with real data."""
        # Test with common word
        comedy_tags = tags_instance.tags_with("comedy")

        assert isinstance(comedy_tags, list)
        assert len(comedy_tags) > 0

        # Check sorting (alphabetical)
        assert comedy_tags == sorted(comedy_tags)

        # Check that all returned tags contain the word
        for tag in comedy_tags:
            assert "comedy" in tag.lower()

        # Test with less common word
        scifi_tags = tags_instance.tags_with("sci-fi")
        assert len(scifi_tags) > 0
        for tag in scifi_tags:
            assert "sci-fi" in tag.lower()

        # Test case insensitivity
        funny_tags_upper = tags_instance.tags_with("FUNNY")
        funny_tags_lower = tags_instance.tags_with("funny")
        assert funny_tags_upper == funny_tags_lower

        # Test with non-existent word
        nonexistent_tags = tags_instance.tags_with("nonexistentwordxyz")
        assert len(nonexistent_tags) == 0

    def test_tags_edge_cases(self, tags_instance: Tags):
        """Test edge cases for Tags methods."""
        # Test with n=0
        assert tags_instance.most_words(0) == {}
        assert tags_instance.longest(0) == []
        assert tags_instance.most_popular(0) == {}

        # Test with n larger than dataset
        large_n = tags_instance.most_words(10000)
        assert len(large_n) <= len(tags_instance.data)

        # Test empty string in tags_with
        empty_tags = tags_instance.tags_with("")
        assert len(empty_tags) > 0  # Should return all unique tags


@pytest.mark.skipif(not os.path.exists(MOVIES_FILE), reason="Data files not found")
@pytest.mark.skipif(not os.path.exists(LINKS_FILE), reason="Data files not found")
class TestLinksIntegration:
    """Integration tests for the Ratings class using real data."""

    @pytest.fixture(scope="class")
    def movies_instance(self):
        """Fixture to create a Movies instance for integration tests."""
        return Movies(MOVIES_FILE)

    @pytest.fixture(scope="class")
    def links_instance(self, movies_instance: Movies):
        """Fixture to create a Ratings instance for integration tests."""
        return Links(LINKS_FILE, movies=movies_instance)

    def test_get_imdb_integration(self, links_instance: Links):
        """Test get_imdb method with real data."""
        # Testing on several famous films
        test_movies = [1, 2, 3]  # Toy Story, Jumanji, Grumpier Old Men

        imdb_data = links_instance.get_imdb(test_movies)

        assert isinstance(imdb_data, list)

        # Check the data structure
        for movie_data in imdb_data:
            assert len(movie_data) == 5
            movie_id, director, budget, gross, runtime = movie_data

            assert isinstance(movie_id, int)
            assert isinstance(director, str)
            assert isinstance(budget, str)
            assert isinstance(gross, str)
            assert isinstance(runtime, int)

            # Check that movie_id is in the original list
            assert movie_id in test_movies

        # Check the sorting in descending order of movie_id
        movie_ids = [item[0] for item in imdb_data]
        assert movie_ids == sorted(movie_ids, reverse=True)
