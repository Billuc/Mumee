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

from mumee.classes import SpotifyOptions
from mumee.data import SongMetadata, PlaylistMetadata
from mumee.errors import MetadataClientError

__all__ = ["SpotifyMetadataClient"]


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

    def get_track(self, url: str) -> SongMetadata:
        if "open.spotify.com" not in url or "track" not in url:
            raise MetadataClientError(f"Invalid Spotify track URL: {url}")

        track_info = self._client.track(url)

        if track_info is None:
            raise MetadataClientError(
                f"Couldn't get metadata associated with this URL: {url}"
            )

        if track_info["duration_ms"] == 0 or track_info["name"].strip() == "":
            raise MetadataClientError(f"Track no longer exists: {url}")

        return self._to_song_metadata(track_info)

    def _to_song_metadata(self, track_info: Dict[str, Any]) -> SongMetadata:
        artist_names = [artist["name"] for artist in track_info["artists"]]
        album_info = self._client.album(track_info["album"]["id"]) or {}

        thumbnails = [
            (tn["width"] * tn["height"], tn["url"]) for tn in album_info["images"]
        ]

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
            duration=int(track_info["duration_ms"] / 1000),
            date=album_info["release_date"],
            year=int(album_info["release_date"][:4]),
            is_song=True,
            id=track_info["id"],
            explicit=track_info["explicit"],
            cover_url=max(thumbnails)[1],
            url=track_info["external_urls"]["spotify"],
        )

        return result

    def get_playlist(self, url: str) -> PlaylistMetadata:
        if "open.spotify.com" not in url or "playlist" not in url:
            raise MetadataClientError(f"Invalid Spotify playlist URL: {url}")

        track_info = self._client.playlist(url)

        if track_info is None:
            raise MetadataClientError(
                f"Couldn't get metadata associated with this URL: {url}"
            )

        result = PlaylistMetadata(
            name=track_info["name"],
            description=track_info["description"],
            author=track_info["owner"]["display_name"],
            tracks=[
                self._to_song_metadata(track["track"])
                for track in track_info["tracks"]["items"]
            ],
        )
        return result

    def search(self, query: str, limit: int, sorted: bool) -> List[SongMetadata]:
        search_results = self._client.search(query)

        if search_results is None or len(search_results["tracks"]["items"]) == 0:
            raise MetadataClientError("No result found for '{query}'")

        if sorted:
            best_results = self._get_best_results(
                query, search_results["tracks"]["items"], limit
            )

            if not best_results or best_results[0][2] < 55:
                raise MetadataClientError(
                    "Best match found isn't close enough to your query. "
                    f"Best match : {best_results[0][1]}, query: {query}"
                )

            results = list(map(lambda r: r[0], best_results))
        else:
            results = list(map(lambda r: r["id"], search_results))[:limit]

        track_infos = [
            self.get_track("http://open.spotify.com/track/" + track) for track in results
        ]
        return track_infos

    def _get_best_results(
        self, query: str, tracks_info: List[Dict[str, Any]], limit: int
    ) -> List[Tuple[str, str, float, float]]:
        results: List[Tuple[str, str, float, float]] = []

        for track in tracks_info:
            track_name = track["name"]
            track_artists = [artist["name"] for artist in track["artists"]]
            track_query = f"{track_name} - {', '.join(track_artists)}"
            track_popularity = track["popularity"]

            score = fuzz.ratio(slugify(track_query), slugify(query))

            results.append((track["id"], track_query, score, track_popularity))

        results = sorted(results, key=lambda t: (t[2], t[3]), reverse=True)
        return results[:limit]
