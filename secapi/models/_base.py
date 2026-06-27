"""Base model shared by every generated response model.

Models accept the API's camelCase JSON (via aliases) but expose clean
``snake_case`` attributes, so ``filing.accession_number`` just works while the
wire format stays ``accessionNumber``. Unknown fields are preserved (``extra``)
so the SDK keeps working when the API adds new fields.
"""

from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class SecBaseModel(BaseModel):
    """Common configuration for all SEC API response models."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
        protected_namespaces=(),
        ser_json_timedelta="iso8601",
    )

    def to_dict(self, *, by_alias: bool = False) -> Dict[str, Any]:
        """Return a plain ``dict`` of the model.

        By default keys are the Python ``snake_case`` names. Pass
        ``by_alias=True`` to get the original API (camelCase) keys.
        """
        return self.model_dump(by_alias=by_alias, exclude_none=True)
