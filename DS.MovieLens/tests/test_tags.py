from unittest.mock import mock_open, patch

from movielens_analytics.tags import Tags


class TestTags:
    """Tests for the Tags class."""

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,tag,timestamp
            1,1,pixar,964982703
            1,1,fun,964982703
            2,2,magic,964982703
            2,2,game,964982703
            """
        ).strip(),
    )
    def test_most_words(self, _):
        """Test the most_words method."""
        tags = Tags("dummy_path")
        expected = {"pixar": 1, "fun": 1, "magic": 1, "game": 1}
        assert tags.most_words(4) == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,tag,timestamp
            1,1,pixar,964982703
            1,1,fun,964982703
            2,2,magic,964982703
            2,2,game,964982703
            """
        ).strip(),
    )
    def test_longest(self, _):
        """Test the longest method."""
        tags = Tags("dummy_path")
        expected = ["pixar", "magic", "game", "fun"]
        assert sorted(tags.longest(4)) == sorted(expected)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,tag,timestamp
            1,1,pixar,964982703
            1,1,fun,964982703
            2,2,magic,964982703
            2,2,game,964982703
            """
        ).strip(),
    )
    def test_most_popular(self, _):
        """Test the most_popular method."""
        tags = Tags("dummy_path")
        expected = {"pixar": 1, "fun": 1, "magic": 1, "game": 1}
        assert tags.most_popular(4) == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,tag,timestamp
            1,1,pixar,964982703
            1,1,fun,964982703
            2,2,magic,964982703
            2,2,game,964982703
            """
        ).strip(),
    )
    def test_tags_with(self, _):
        """Test the tags_with method."""
        tags = Tags("dummy_path")
        expected = ["magic"]
        assert tags.tags_with("magic") == expected

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            """
            userId,movieId,tag,timestamp
            1,1,a long tag,964982703
            1,1,short,964982703
            2,2,another long tag,964982703
            2,2,tag,964982703
            """
        ).strip(),
    )
    def test_most_words_and_longest(self, _):
        """Test the most_words_and_longest method."""
        tags = Tags("dummy_path")
        expected = ["a long tag", "another long tag"]
        assert sorted(tags.most_words_and_longest(2)) == sorted(expected)
