"""Auto-generated SEC API models. Do not edit by hand.

Regenerate with: python scripts/generate_models.py
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ._base import SecBaseModel


class ApiError(SecBaseModel):
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


class ErrorResponse(SecBaseModel):
    error: Optional[ApiError] = None


__all__ = [
    "ApiError",
    "ErrorResponse",
]

for _m in list(globals().values()):
    if isinstance(_m, type) and issubclass(_m, SecBaseModel):
        _m.model_rebuild()
