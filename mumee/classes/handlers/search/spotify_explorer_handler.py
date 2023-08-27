from typing import Callable, List, Optional

from mumee.interfaces import BaseMetadataExplorer
from mumee.classes import SpotifyMetadataClient
from mumee.data import SearchMetadataCommand, SongMetadata, MetadataClientEnum

__all__ = ["SpotifyExplorerHandler"]


class SpotifyExplorerHandler(BaseMetadataExplorer):
    def __init__(self, client: SpotifyMetadataClient) -> None:
        super().__init__()
        self._client = client

    def _handle(
        self,
        request: SearchMetadataCommand,
        next: Callable[[SearchMetadataCommand], Optional[List[SongMetadata]]],
    ) -> Optional[List[SongMetadata]]:
        if (
            MetadataClientEnum.ALL not in request.clients
            and MetadataClientEnum.SPOTIFY not in request.clients
        ):
            return next(request)

        previous_results = next(request) or []

        spotify_results = self._client.search(
            request.query, request.limit_per_client, request.sorted
        )

        return [*previous_results, *spotify_results]
