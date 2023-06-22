from taipan_di import ServiceCollection

from song_metadata_client.classes import (
    SpotifyOptions,
    SpotifyMetadataClient,
    YTMusicMetadataClient,
)
from song_metadata_client.classes.handlers import *
from song_metadata_client.interfaces import BaseMetadataClient

__all__ = ["add_song_metadata_client"]


def add_song_metadata_client(services: ServiceCollection) -> ServiceCollection:
    services.register(SpotifyOptions).as_singleton().with_self()

    services.register(SpotifyMetadataClient).as_factory().with_self()
    services.register(YTMusicMetadataClient).as_factory().with_self()

    services.register_pipeline(BaseMetadataClient).add(SpotifyTrackHandler).add(
        SpotifyPlaylistHandler
    ).add(YTMusicTrackHandler).add(YTMusicPlaylistHandler).add(SpotifySearchHandler).add(
        YTMusicSearchHandler
    ).as_factory()

    return services
