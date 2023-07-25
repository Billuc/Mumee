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

        number_of_clients = (
            len(MetadataClientEnum) - 1
            if MetadataClientEnum.ALL in request.clients
            else len(request.clients)
        )
        client_limit = int(request.limit / number_of_clients) # TODO : edge case when limit < number of clients

        spotify_results = self._client.search(request.query, client_limit)

        return [*previous_results, *spotify_results]
