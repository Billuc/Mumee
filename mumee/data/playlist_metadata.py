from dataclasses import dataclass
from typing import List

from mumee.data import SongMetadata

__all__ = ["PlaylistMetadata"]


@dataclass
class PlaylistMetadata:
    name: str
    description: str
    author: str
    tracks: List[SongMetadata]
