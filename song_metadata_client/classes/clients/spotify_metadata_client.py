from typing import Any, Dict, List, Tuple
from spotipy import (
    Spotify,
    CacheFileHandler,
    MemoryCacheHandler,
    SpotifyOAuth,
    SpotifyClientCredentials,
)
from rapidfuzz import fuzz
from slugify import slugify

from song_metadata_client.classes import SongMetadata, SpotifyOptions
from song_metadata_client.errors import MetadataClientError


class SpotifyMetadataClient:
    def __init__(self, options: SpotifyOptions) -> None:
        cache_handler = (
            CacheFileHandler(options.cache_path)
            if options.use_cache
            else MemoryCacheHandler()
        )

        if options.auth_token is not None:
            credentials_manager = None
        elif options.use_auth:
            credentials_manager = SpotifyOAuth(
                client_id=options.client_id,
                client_secret=options.client_secret,
                redirect_uri="http://127.0.0.1:8080/",
                scope="user-library-read",
                cache_handler=cache_handler,
                open_browser=not options.headless,
            )
        else:
            credentials_manager = SpotifyClientCredentials(
                client_id=options.client_id,
                client_secret=options.client_secret,
                cache_handler=cache_handler,
            )

        self._client = Spotify(
            auth=options.auth_token,
            auth_manager=credentials_manager,
            status_forcelist=(429, 500, 502, 503, 504, 404),
        )

    def get_from_url(self, url: str) -> SongMetadata:
        if "open.spotify.com" not in url or "track" not in url:
            raise MetadataClientError(f"Invalid Spotify track URL: {url}")

        track_info = self._client.track(url)

        if track_info is None:
            raise MetadataClientError(
                f"Couldn't get metadata associated with this URL : {url}"
            )

        if track_info["duration_ms"] == 0 or track_info["name"].strip() == "":
            raise MetadataClientError(f"Track no longer exists: {url}")

        artist_names = [artist["name"] for artist in track_info["artists"]]
        album_info = self._client.album(track_info["album"]["id"])

        result = SongMetadata(
            name=track_info["name"],
            artists=artist_names,
            artist=artist_names[0],
            album_name=album_info["name"],
            album_artist=album_info["artists"][0]["name"],
            disc_number=track_info["disc_number"],
            disc_count=int(album_info["tracks"]["items"][-1]["disc_number"]),
            track_number=track_info["track_number"],
            track_count=album_info["total_tracks"],
            genres=album_info["genres"],
            duration=track_info["duration_ms"] / 1000,
            date=album_info["release_date"],
            year=int(album_info["release_date"][:4]),
        )

        return result

    def search(self, query: str) -> SongMetadata:
        search_results = self._client.search(query)

        if search_results is None or len(search_results["tracks"]["items"]) == 0:
            raise MetadataClientError("No result found for '{query}'")

        best_result = self._get_best_result(query, search_results["tracks"]["items"])

        if best_result[2] < 55:
            raise MetadataClientError(
                "Best match found isn't close enough to your query. "
                f"Best match : {best_result[1]}, query: {query}"
            )

        song_url = "http://open.spotify.com/track/" + best_result[0]
        return self.get_from_url(song_url)

    def _get_best_result(
        self, query: str, tracks_info: List[Dict[str, Any]]
    ) -> Tuple[str, str, int]:
        best_score = 0
        best_id = None
        best_query = None
        best_popularity = 0

        for track in tracks_info:
            track_name = track["name"]
            track_artists = [artist["name"] for artist in track["artists"]]
            track_query = f"{track_name} - {', '.join(track_artists)}"
            track_popularity = track["popularity"]

            score = fuzz.ratio(slugify(track_query), slugify(query))

            if score > best_score or (
                score == best_score and track_popularity > best_popularity
            ):
                best_score = score
                best_id = track["id"]
                best_query = track_query
                best_popularity = track_popularity

        return best_id, best_query, best_score
