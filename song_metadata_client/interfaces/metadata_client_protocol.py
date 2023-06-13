from typing import Protocol
from song_metadata_client.classes import SongMetadata

class MetadataClientProtocol(Protocol):
    def get_from_url(self, url: str) -> SongMetadata:
        ...
    
    def search(self, query: str) -> SongMetadata:
        ...