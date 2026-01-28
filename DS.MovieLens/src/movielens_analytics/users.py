import statistics
from dataclasses import dataclass, field

from .ratings import Rating, Ratings


@dataclass
class User:
    """Represents a user with their ID and a list of ratings."""

    user_id: int
    ratings: list[Rating] = field(default_factory=list[Rating])


class Users:
    """
    Provides methods for analyzing user behavior based on ratings data.
    """

    data: dict[int, User]

    def __init__(self, ratings: Ratings):
        """Initializes the Users object with ratings data."""
        self.data = {}
        for rating in ratings.data:
            if rating.user_id not in self.data:
                self.data[rating.user_id] = User(user_id=rating.user_id)
            self.data[rating.user_id].ratings.append(rating)

    def dist_by_num_of_ratings(self) -> dict[int, int]:
        """
        Calculates the distribution of users by the number of ratings they have made.
        Returns a dict of {user_id: count}, sorted by user_id.
        """
        user_counts = {user.user_id: len(user.ratings) for user in self.data.values()}
        return dict(sorted(user_counts.items()))

    def dist_by_rating_metric(self, metric: str = "average") -> dict[int, float]:
        """
        Calculates the distribution of users by their average or median rating.
        Returns a dict of {user_id: metric_value}, sorted by user_id.
        """
        user_metrics: dict[int, float] = {}
        for user_id, user in self.data.items():
            ratings_list = [rating.rating for rating in user.ratings]
            if not ratings_list:
                continue
            if metric == "average":
                user_metrics[user_id] = round(statistics.mean(ratings_list), 2)
            elif metric == "median":
                user_metrics[user_id] = round(statistics.median(ratings_list), 2)

        return dict(sorted(user_metrics.items()))

    def top_by_variance(self, n: int) -> dict[int, float]:
        """
        Finds the top-n users with the highest rating variance.
        Returns a dict of {user_id: variance}, sorted by variance descendingly.
        """
        user_variances: dict[int, float] = {}
        for user_id, user in self.data.items():
            ratings_list = [rating.rating for rating in user.ratings]
            if len(ratings_list) > 1:
                user_variances[user_id] = round(statistics.variance(ratings_list), 2)

        sorted_users: list[tuple[int, float]] = sorted(
            user_variances.items(), key=lambda item: item[1], reverse=True
        )
        return dict(sorted_users[:n])
