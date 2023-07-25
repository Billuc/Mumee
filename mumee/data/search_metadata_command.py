from dataclasses import dataclass, field
from typing import List

from mumee.data import MetadataClientEnum

__all__ = ["SearchMetadataCommand"]


@dataclass
class SearchMetadataCommand:
    query: str
    clients: List[MetadataClientEnum] = field(default_factory=lambda: [MetadataClientEnum.ALL])
    limit: int = 10
