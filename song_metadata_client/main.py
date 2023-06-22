from typing import Optional, Union
from taipan_di import ServiceCollection

from song_metadata_client.classes import SongMetadata, PlaylistMetadata, SpotifyOptions
from song_metadata_client.di import add_song_metadata_client
from song_metadata_client.interfaces import BaseMetadataClient
from song_metadata_client.errors import MetadataClientError


class SongMetadataClient:
    def __init__(self, spotify_options: Optional[SpotifyOptions] = None):
        services = ServiceCollection()
        add_song_metadata_client(services)

        if spotify_options is not None:
            services.register(SpotifyOptions).as_singleton().with_instance(spotify_options)

        self._client = services.build().resolve(BaseMetadataClient)

    def search(self, url_or_query: str) -> Union[SongMetadata, PlaylistMetadata]:
        result = self._client.exec(url_or_query)

        if result is None:
            raise MetadataClientError("No result")

        return result
