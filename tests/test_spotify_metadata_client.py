from song_metadata_client.classes import SpotifyOptions, SpotifyMetadataClient
from song_metadata_client.errors import MetadataClientError
from tests.my_vcr import generate_vcr

my_vcr = generate_vcr("test_spotify_metadata_client")


def test_init_client():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)


@my_vcr.use_cassette
def test_get_track():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    metadata = client.get_track(
        "https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr?si=5cc9c24b381446f7"
    )

    assert metadata is not None
    assert metadata.artist == "Linkin Park"
    assert metadata.name == "Faint"
    assert metadata.album_name == "Meteora (Bonus Edition)"
    assert metadata.year == 2003


def test_get_track_error_if_spotify_not_in_url():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    try:
        client.get_track("https://www.youtube.com/123654")
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


def test_get_track_error_if_track_not_in_url():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    try:
        client.get_track("https://open.spotify.com/album/foobar")
        assert False
    except MetadataClientError:
        assert True
    except:
        assert False


@my_vcr.use_cassette
def test_get_track_error_if_wrong_url():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    try:
        client.get_track("https://open.spotify.com/track/foobar")
        assert False
    except Exception as ex:
        assert True


@my_vcr.use_cassette
def test_get_playlist():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    metadata = client.get_playlist(
        "https://open.spotify.com/playlist/37i9dQZF1DX8FwnYE6PRvL?si=5247b1174845492b"
    )

    assert metadata is not None
    assert metadata.name == "Rock Party"
    assert metadata.description == "The ultimate rock party playlist!"
    assert metadata.author == "Spotify"
    assert any(track.name == "Dance, Dance" for track in metadata.tracks)


def test_get_playlist_error_if_spotify_not_in_url():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    try:
        client.get_playlist("https://www.youtube.com/123654")
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


def test_get_playlist_error_if_playlist_not_in_url():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    try:
        client.get_playlist("https://open.spotify.com/album/foobar")
        assert False
    except MetadataClientError:
        assert True
    except:
        assert False


@my_vcr.use_cassette
def test_get_playlist_error_if_wrong_url():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    try:
        client.get_playlist("https://open.spotify.com/playlist/foobar")
        assert False
    except Exception as ex:
        assert True


@my_vcr.use_cassette
def test_search():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    metadata = client.search("Faint - Linkin Park")

    assert metadata is not None
    assert metadata.artist == "Linkin Park"
    assert metadata.name == "Faint"
    assert metadata.album_name == "Meteora"


@my_vcr.use_cassette
def test_search_error_if_bad_results():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)

    try:
        metadata = client.search("foo bar baz azerazrqrsrtxv")
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False
