# Copyright 2022 The HuggingFace Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
""" Sensors for the RL Agent."""
import itertools
from cmath import inf
from dataclasses import InitVar, dataclass
from typing import Any, ClassVar, List, Optional, Union

import numpy as np
from dataclasses_json import dataclass_json

from simulate import logging

from .asset import Asset
from .gltf_extension import GltfExtensionMixin


logger = logging.get_logger(__name__)

try:
    from gym import spaces
except ImportError:
    # Our implementation of gym space classes if gym is not installed
    logger.warning(
        "The gym library is not installed, falling back our implementation of gym.spaces. To remove this message pip install simulate[rl]"
    )
    from . import spaces


ALLOWED_STATE_SENSOR_PROPERTIES = {
    "position": 3,
    "position.x": 1,
    "position.y": 1,
    "position.z": 1,
    "velocity": 3,
    "velocity.x": 1,
    "velocity.y": 1,
    "velocity.z": 1,
    "rotation": 3,
    "rotation.x": 1,
    "rotation.y": 1,
    "rotation.z": 1,
    "angular_velocity": 3,
    "angular_velocity.x": 1,
    "angular_velocity.y": 1,
    "angular_velocity.z": 1,
    "distance": 1,
}


def get_state_sensor_n_properties(sensor):
    n_features = 0
    for property in sensor.properties:
        n_features += ALLOWED_STATE_SENSOR_PROPERTIES[property]

    return n_features


@dataclass
class StateSensor(Asset, GltfExtensionMixin, gltf_extension_name="HF_state_sensors", object_type="node"):
    """A State sensor: pointer to two assets whose positions/rotations are used to compute an observation

    Attributes:
        target_entity: Reference (or string name) of the target Asset in the scene
        reference_entity: Reference (or string name) of the reference Asset in the scene
            If no reference is provided we use the world as a reference
        type: How should we compute the observation, selected in the list of:
            - "position": the position of the target asset
            - "rotation": the rotation of the target asset
            - "distance": the distance to the target asset (default)
    """

    target_entity: Optional[Any] = None
    reference_entity: Optional[Any] = None
    properties: Optional[List[str]] = None
    sensor_tag: str = "StateSensor"

    name: InitVar[Optional[str]] = None
    position: InitVar[Optional[List[float]]] = None
    rotation: InitVar[Optional[List[float]]] = None
    scaling: InitVar[Optional[Union[float, List[float]]]] = None
    transformation_matrix: InitVar[Optional[List[float]]] = None
    parent: InitVar[Optional[Any]] = None
    children: InitVar[Optional[List[Any]]] = None
    created_from_file: InitVar[Optional[str]] = None

    __NEW_ID: ClassVar[Any] = itertools.count()  # Singleton to count instances of the classes for automatic naming

    def __post_init__(
        self, name, position, rotation, scaling, transformation_matrix, parent, children, created_from_file
    ):
        super().__init__(
            name=name,
            position=position,
            rotation=rotation,
            scaling=scaling,
            transformation_matrix=transformation_matrix,
            parent=parent,
            children=children,
            created_from_file=created_from_file,
        )

        if self.properties is None:
            self.properties = ["distance"]
        if not isinstance(self.properties, (list, tuple)):
            self.properties = [self.properties]
        elif any(properties_ not in ALLOWED_STATE_SENSOR_PROPERTIES for properties_ in self.properties):
            raise ValueError(
                f"The properties {self.properties} is not a valid StateSensor properties"
                f"\nAllowed properties are: {ALLOWED_STATE_SENSOR_PROPERTIES}"
            )

    @property
    def observation_space(self):
        return spaces.Box(low=-inf, high=inf, shape=[get_state_sensor_n_properties(self)], dtype=np.float32)


@dataclass_json
@dataclass
class RaycastSensor(Asset, GltfExtensionMixin, gltf_extension_name="HF_raycast_sensors", object_type="node"):
    """A Raycast sensor: cast a ray to get an observation"""

    n_horizontal_rays: int = 1
    n_vertical_rays: int = 1
    horizontal_fov: float = 0
    vertical_fov: float = 0
    ray_length: float = 100
    sensor_tag: str = "RaycastSensor"

    name: InitVar[Optional[str]] = None
    position: InitVar[Optional[List[float]]] = None
    rotation: InitVar[Optional[List[float]]] = None
    scaling: InitVar[Optional[Union[float, List[float]]]] = None
    transformation_matrix: InitVar[Optional[List[float]]] = None
    parent: InitVar[Optional[Any]] = None
    children: InitVar[Optional[List[Any]]] = None
    created_from_file: InitVar[Optional[str]] = None

    __NEW_ID: ClassVar[Any] = itertools.count()  # Singleton to count instances of the classes for automatic naming

    def __post_init__(
        self, name, position, rotation, scaling, transformation_matrix, parent, children, created_from_file
    ):
        super().__init__(
            name=name,
            position=position,
            rotation=rotation,
            scaling=scaling,
            transformation_matrix=transformation_matrix,
            parent=parent,
            children=children,
            created_from_file=created_from_file,
        )

    @property
    def observation_space(self):
        return spaces.Box(low=-inf, high=inf, shape=[self.n_horizontal_rays * self.n_vertical_rays], dtype=np.float32)