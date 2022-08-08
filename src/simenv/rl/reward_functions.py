from dataclasses import dataclass
from typing import Any, Optional


ALLOWED_REWARD_TYPES = ["dense", "sparse", "or", "and", "not", "see", "timeout"]
ALLOWED_REWARD_DISTANCE_METRICS = ["euclidean"]  # TODO(Ed) other metrics?


@dataclass
class RewardFunction:
    """An RL reward function

    Attributes:
        type: str, optional (default="dense")
            The type of reward function. Must be one of the following:
                "dense"
                "sparse"
        entity_a: Asset
            The first entity in the reward function
        entity_b: Asset
            The second entity in the reward function
        distance_metric: str, optional (default="euclidean")
            The distance metric to use. Must be one of the following:
                "euclidean"
        scalar: float, optional (default=1.0)
            The scalar reward
        threshold: float, optional (default=0.0)
            The distance threshold to give the reward
        is_terminal: bool, optional (default=False)
            Whether the reward is terminal
        is_collectable: bool, optional (default=False)
            Whether the reward is collectable
        trigger_once: bool, optional (default=False)
            Whether the reward is triggered once
        reward_function_a: RewardFunction, optional (default=None)
            When doing combination of rewards (and, or), the first reward function
        reward_function_b: RewardFunction, optional (default=None)
            When doing combination of rewards (and, or), the second reward function
    """

    entity_a: Any
    entity_b: Any
    type: Optional[str] = None
    distance_metric: Optional[str] = None
    scalar: Optional[float] = 1.0
    threshold: Optional[float] = 1.0
    is_terminal: Optional[bool] = False
    is_collectable: Optional[bool] = False
    trigger_once: Optional[bool] = True
    reward_function_a: Optional["RewardFunction"] = None
    reward_function_b: Optional["RewardFunction"] = None

    def __post_init__(self):
        if self.type is None:
            self.type = "dense"
        if self.type not in ALLOWED_REWARD_TYPES:
            raise ValueError(f"Invalid reward type: {self.type}. Must be one of: {ALLOWED_REWARD_TYPES}")
        if self.distance_metric is None:
            self.distance_metric = "euclidean"
        if self.distance_metric not in ALLOWED_REWARD_DISTANCE_METRICS:
            raise ValueError(
                f"Invalid distance metric: {self.distance_metric}. Must be one of: {ALLOWED_REWARD_DISTANCE_METRICS}"
            )

    def _post_copy(self, agent: Any):
        root = agent.tree_root

        new_instance = type(self)(
            type=self.type,
            entity_a=root.get_node(self.entity_a._get_last_copy_name()),
            entity_b=root.get_node(self.entity_b._get_last_copy_name()),
            distance_metric=self.distance_metric,
            scalar=self.scalar,
            threshold=self.threshold,
            is_terminal=self.is_terminal,
            is_collectable=self.is_collectable,
            trigger_once=self.trigger_once,
            reward_function_a=self.reward_function_a,
            reward_function_b=self.reward_function_b,
        )

        return new_instance