from typing import Callable, Union

from song_metadata_client.interfaces import BaseMetadataClient
from song_metadata_client.classes import (
    SpotifyMetadataClient,
    SongMetadata,
    PlaylistMetadata,
)


class SpotifyTrackHandler(BaseMetadataClient):
    def __init__(self, client: SpotifyMetadataClient) -> None:
        self._client = client

    def _handle(
        self, request: str, next: Callable[[str], Union[SongMetadata, PlaylistMetadata]]
    ) -> Union[SongMetadata, PlaylistMetadata]:
        if "open.spotify.com" not in request or "track" not in request:
            return next(request)

        return self._client.get_track(request)
