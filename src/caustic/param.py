from typing import Optional, Tuple

import torch
from torch import Tensor

__all__ = ("Param",)


class Param:
    """
    Represents a static or dynamic parameter. Static parameters are fixed while
    dynamic parameters must be passed in each time they're required.
    """

    def __init__(self, value: Optional[Tensor] = None, shape: Tuple[int, ...] = ()):
        # Must assign one of value or shape
        self._value = value
        if value is None:
            self._shape = shape
        else:
            if shape is not None and shape != value.shape:
                raise ValueError(
                    f"value's shape {value.shape} does not match provided shape {shape}"
                )

            self._value = value
            self._shape = shape

    @property
    def static(self) -> bool:
        return not self.dynamic

    @property
    def dynamic(self) -> bool:
        return self._value is None

    @property
    def value(self) -> Optional[Tensor]:
        return self._value

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._shape

    def to(
        self, device: Optional[torch.device] = None, dtype: Optional[torch.dtype] = None
    ):
        if self._value is not None:
            self._value = self._value.to(device=device, dtype=dtype)

    def __repr__(self) -> str:
        if not self.dynamic:
            return f"Param(value={self.value})"
        else:
            return f"Param(shape={self.shape})"