from unittest.mock import mock_open, patch

import pytest

from movielens_analytics.movies import Movie, Movies


class TestMovies:
    """
    The `TestMovies` class contains test cases for a `Movies` class that loads movie data from a CSV
    file, handles different scenarios like empty CSV, correctly splits genres, and raises errors for
    invalid data or file paths.
    """

    # Given: CSV with valid movie data
    # When: Movies object is initialized
    # Then: movies dict contains parsed data with split genres
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            movieId,title,genres\n
            1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy\n
            2,Jumanji (1995),Adventure|Children|Fantasy\n
            """
        ).strip(),
    )
    def test_init_loads_movies_correctly(self, _):
        """
        The function tests if the Movies class correctly loads movies from a specified path.

        :param _: The underscore `_` in the function signature
        `test_init_loads_movies_correctly(self, _)` is a convention in Python to indicate that
        the parameter is not going to be used within the function. It's a way to tell other
        developers that the parameter is intentionally ignored.
        """

        # Given
        expected: dict[int, Movie] = {
            1: Movie(
                movie_id=1,
                title="Toy Story (1995)",
                genres=[
                    "Adventure",
                    "Animation",
                    "Children",
                    "Comedy",
                    "Fantasy",
                ],
            ),
            2: Movie(
                movie_id=2,
                title="Jumanji (1995)",
                genres=["Adventure", "Children", "Fantasy"],
            ),
        }

        # When
        movies = Movies("dummy_path")

        # Then
        assert movies.data == expected

    # Given: CSV with only header (no data rows)
    # When: Movies object is initialized
    # Then: movies dict is empty
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="movieId,title,genres\n",
    )
    def test_init_handles_empty_csv(self, _):
        """
        The function tests that the initialization of a Movies object handles an empty CSV file
        correctly.

        :param _: The "_" parameter in the test_init_handles_empty_csv method is typically used as a
        placeholder for a parameter that is not being used in the test case. In this case, it seems
        that the test case does not require the second parameter for any specific functionality,
        so it is simply represented as "_"
        """
        # When
        movies = Movies("dummy_path")

        # Then
        assert not movies.data

    # Given: CSV with multiple movies with different genres
    # When: Movies object is initialized
    # Then: genres are correctly split by pipe delimiter
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            movieId,title,genres\n
            1,Toy Story (1995),Adventure|Animation\n
            2,Jumanji (1995),Adventure|Children\n
            """
        ).strip(),
    )
    def test_genres_split_correctly(self, _):
        """
        This function tests whether genres are split correctly in a Movies object.

        :param _: The "_" parameter in the test_genres_split_correctly method is typically used to
        represent a placeholder for a parameter that is not being used in the test case.
        In this case, it seems that the test_genres_split_correctly method does not require any
        additional parameters for the test scenario being executed
        """
        # When
        movies = Movies("dummy_path")

        # Then
        assert movies.data[1].genres == ["Adventure", "Animation"]
        assert movies.data[2].genres == ["Adventure", "Children"]

    # Given: CSV with invalid movieId (non-numeric)
    # When: Movies object is initialized
    # Then: ValueError is raised
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            movieId,title,genres\n
            abc,Toy Story (1995),Adventure\n
            """
        ).strip(),
    )
    def test_handles_invalid_movieid(self, _):
        """
        The function tests if an exception is raised when an invalid movie ID is provided.

        :param _: The underscore (_) in the function signature is typically used as a placeholder
        for a parameter that is not being used within the function. In this case, it seems that
        the second parameter is not being used in the test_handles_invalid_movieid function
        """
        # When/Then
        with pytest.raises(ValueError):
            Movies("dummy_path")

    # Given: Non-existent file path
    # When: Movies object is initialized
    # Then: FileNotFoundError is raised
    def test_init_raises_file_not_found(self):
        """
        The function tests that an error is raised when trying to initialize a Movies object with a
        nonexistent file path.
        """
        # When/Then
        with pytest.raises(FileNotFoundError):
            Movies("nonexistent_path")

    @patch(
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
    )
    def test_dist_by_release(self, _):
        """Test the dist_by_release method."""
        movies = Movies("dummy_path")
        expected = {1995: 3}
        assert movies.dist_by_release() == expected

    @patch(
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
    )
    def test_dist_by_genres(self, _):
        """Test the dist_by_genres method."""
        movies = Movies("dummy_path")
        expected = {
            "Adventure": 2,
            "Children": 2,
            "Comedy": 2,
            "Fantasy": 2,
            "Animation": 1,
            "Romance": 1,
        }
        # The order of items with the same value is not guaranteed, so we compare dicts
        # after sorting them by value, then key
        assert sorted(
            movies.dist_by_genres().items(), key=lambda item: (-item[1], item[0])
        ) == sorted(expected.items(), key=lambda item: (-item[1], item[0]))

    @patch(
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
    )
    def test_most_genres(self, _):
        """Test the most_genres method."""
        movies = Movies("dummy_path")
        expected = {"Toy Story (1995)": 5, "Jumanji (1995)": 3}
        assert movies.most_genres(2) == expected
