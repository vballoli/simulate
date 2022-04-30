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
""" A simenv Asset - Objects in the scene (mesh, primitives, camera, lights)."""
import math
import uuid
from typing import Optional

import numpy as np

from .anytree import NodeMixin


def quat_from_euler(x, y, z):
    qx = np.sin(x / 2) * np.cos(y / 2) * np.cos(z / 2) - np.cos(x / 2) * np.sin(y / 2) * np.sin(z / 2)
    qy = np.cos(x / 2) * np.sin(y / 2) * np.cos(z / 2) + np.sin(x / 2) * np.cos(y / 2) * np.sin(z / 2)
    qz = np.cos(x / 2) * np.cos(y / 2) * np.sin(z / 2) - np.sin(x / 2) * np.sin(y / 2) * np.cos(z / 2)
    qw = np.cos(x / 2) * np.cos(y / 2) * np.cos(z / 2) + np.sin(x / 2) * np.sin(y / 2) * np.sin(z / 2)
    return [qx, qy, qz, qw]


def quat_from_degrees(x, y, z):
    return quat_from_euler(math.radians(x), math.radians(y), math.radians(z))


class Asset(NodeMixin, object):
    dimensionality = 3  # 2 for bi-dimensional assets and 3 for tri-dimensional assets (default is 3)

    def __init__(
        self, name: Optional[str] = None, translation=None, rotation=None, scale=None, parent=None, children=None
    ):
        self.name = name or self.__class__.__name__
        self.id = uuid.uuid4()

        self.parent = parent
        if children:
            self.children = children

        self.translation = translation
        self.rotation = rotation
        self.scale = scale

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, value):
        if self.dimensionality == 3:
            if value is None:
                value = [0.0, 0.0, 0.0]
            elif len(value) != 3:
                raise ValueError("Translation should be of size 3 (X, Y, Z)")
        elif self.dimensionality == 2:
            raise NotImplementedError()
        self._translation = tuple(value)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if self.dimensionality == 3:
            if value is None:
                value = [0.0, 0.0, 0.0, 0.0]
            elif len(value) == 3:
                value = quat_from_euler(*value)
            elif len(value) != 4:
                raise ValueError("Rotation should be of size 3 (Euler angles) or 4 (Quaternions")
        elif self.dimensionality == 2:
            raise NotImplementedError()
        self._rotation = tuple(value)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if self.dimensionality == 3:
            if value is None:
                value = [1.0, 1.0, 1.0]
            elif len(value) == 1:
                value = [value, value, value]
            elif len(value) != 3:
                raise ValueError("Scale should be of size 1 (Uniform scale) or 3 (X, Y, Z)")
        elif self.dimensionality == 2:
            raise NotImplementedError()
        self._scale = tuple(value)

    def __repr__(self):
        return f"{self.name} ({self.__class__.__name__})"


class World3D(Asset):
    dimensionality = 3