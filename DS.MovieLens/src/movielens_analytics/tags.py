import csv
from collections import Counter
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Tag:
    """Represents a single tag."""

    user_id: int
    movie_id: int
    tag: str
    timestamp: datetime


class Tags:
    """Analyzing data from tags.csv"""

    path: str
    data: list[Tag]

    def __init__(self, path_to_the_file: str):
        """
        Initializes the Tags object, loading tag data from the specified file.
        """
        self.path = path_to_the_file
        self.data: list[Tag] = self._load_tags()

    def _load_tags(self) -> list[Tag]:
        """Loads tags from the CSV file into a list of Tag objects."""
        tags_data: list[Tag] = []
        with open(self.path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tags_data.append(
                    Tag(
                        user_id=int(row["userId"]),
                        movie_id=int(row["movieId"]),
                        tag=row["tag"],
                        timestamp=datetime.fromtimestamp(int(row["timestamp"])),
                    )
                )
        return tags_data

    def most_words(self, n: int) -> dict[str, int]:
        """
        Finds the top-n tags with the most words.
        Returns a dict where keys are tags and values are word counts, sorted descendingly.
        """
        tag_word_counts = {tag.tag: len(tag.tag.split()) for tag in self.data}
        sorted_tags = sorted(tag_word_counts.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_tags[:n])

    def longest(self, n: int) -> list[str]:
        """
        Finds the top-n longest tags by character count.
        Returns a list of unique tags, sorted by length descendingly.
        """
        tags = sorted({tag.tag for tag in self.data}, key=len, reverse=True)
        return tags[:n]

    def most_words_and_longest(self, n: int) -> list[str]:
        """
        Finds the intersection of the top-n most-worded and top-n longest tags.
        Returns a list of unique tags.
        """
        most_words_tags = list(self.most_words(n).keys())
        longest_tags = self.longest(n)
        return list(set(most_words_tags) & set(longest_tags))

    def most_popular(self, n: int) -> dict[str, int]:
        """
        Finds the top-n most popular tags by frequency.
        Returns a dict where keys are tags and values are counts, sorted descendingly.
        """
        tag_counts = Counter(tag.tag for tag in self.data)
        return dict(tag_counts.most_common(n))

    def tags_with(self, word: str) -> list[str]:
        """
        Finds all unique tags containing a specific word.
        Returns a list of tags, sorted alphabetically.
        """
        tags = sorted({tag.tag for tag in self.data if word.lower() in tag.tag.lower()})
        return tags
