from typing import Callable, Union

from song_metadata_client.interfaces import BaseMetadataClient
from song_metadata_client.classes import (
    YTMusicMetadataClient,
    SongMetadata,
    PlaylistMetadata,
)


class YTMusicTrackHandler(BaseMetadataClient):
    def __init__(self, client: YTMusicMetadataClient) -> None:
        super().__init__()
        self._client = client

    def _handle(
        self, request: str, next: Callable[[str], Union[SongMetadata, PlaylistMetadata]]
    ) -> Union[SongMetadata, PlaylistMetadata]:
        if "music.youtube.com" not in request or "watch?v" not in request:
            return next(request)

        return self._client.get_track(request)
