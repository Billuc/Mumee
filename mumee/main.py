from typing import List, Optional, Union
from taipan_di import ServiceCollection

from mumee.classes import SpotifyOptions
from mumee.data import (
    SongMetadata,
    PlaylistMetadata,
    SearchMetadataCommand,
    MetadataClientEnum,
)
from mumee.di import add_mumee
from mumee.interfaces import BaseMetadataClient, BaseMetadataExplorer
from mumee.errors import MetadataClientError


class SongMetadataClient:
    def __init__(self, spotify_options: Optional[SpotifyOptions] = None):
        services = ServiceCollection()
        add_mumee(services)

        if spotify_options is not None:
            services.register(SpotifyOptions).as_singleton().with_instance(spotify_options)

        provider = services.build()

        self._fetcher = provider.resolve(BaseMetadataClient)
        self._explorer = provider.resolve(BaseMetadataExplorer)

    def fetch(self, url_or_query: str) -> Union[SongMetadata, PlaylistMetadata]:
        result = self._fetcher.exec(url_or_query)

        if result is None:
            raise MetadataClientError(f"No result for query {url_or_query}")

        return result

    def search(
        self,
        query: str,
        limit: int,
        clients: List[MetadataClientEnum] = [MetadataClientEnum.ALL],
        sorted: bool = True,
    ) -> List[SongMetadata]:
        command = SearchMetadataCommand(query, clients, limit, sorted)
        results = self._explorer.exec(command)

        return results or []
