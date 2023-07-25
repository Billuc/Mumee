from mumee import SongMetadataClient, MetadataClientError, SongMetadata, PlaylistMetadata
from tests.my_vcr import generate_vcr

my_vcr = generate_vcr("test_song_metadata_client")


def test_init_client():
    client = SongMetadataClient()


@my_vcr.use_cassette
def test_fetch_spotify_track():
    client = SongMetadataClient()

    metadata = client.fetch(
        "https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr?si=5cc9c24b381446f7"
    )

    assert metadata is not None
    assert isinstance(metadata, SongMetadata)
    assert metadata.artist == "Linkin Park"
    assert metadata.name == "Faint"
    assert metadata.album_name == "Meteora (Bonus Edition)"
    assert metadata.year == 2003


@my_vcr.use_cassette
def test_fetch_spotify_playlist():
    client = SongMetadataClient()

    metadata = client.fetch(
        "https://open.spotify.com/playlist/37i9dQZF1DX8FwnYE6PRvL?si=a53b50c5637f420b"
    )

    assert metadata is not None
    assert isinstance(metadata, PlaylistMetadata)
    assert metadata.name == "Rock Party"
    assert metadata.description == "The ultimate rock party playlist!"
    assert metadata.author == "Spotify"
    assert any(track.name == "Dance, Dance" for track in metadata.tracks)


@my_vcr.use_cassette
def test_fetch_ytmusic_track():
    client = SongMetadataClient()

    metadata = client.fetch("https://music.youtube.com/watch?v=c6i88Y7gDl4&feature=share")

    assert metadata is not None
    assert isinstance(metadata, SongMetadata)
    assert metadata.artist == "I Prevail"
    assert metadata.name == "Deep End"
    assert metadata.album_name == "TRUE POWER"
    assert metadata.year == 2022


@my_vcr.use_cassette
def test_fetch_ytmusic_playlist():
    client = SongMetadataClient()

    metadata = client.fetch(
        "https://music.youtube.com/playlist?list=RDCLAK5uy_keb_mIiClglpMd5ycINvnTwCkoIu5Ce3k"
    )

    assert metadata is not None
    assert isinstance(metadata, PlaylistMetadata)
    assert metadata.name == "'00s Rock"
    assert metadata.author == "YouTube Music"
    assert metadata.description.startswith("New millennium rock and roll!")
    assert any(track.name == "Numb" for track in metadata.tracks)


@my_vcr.use_cassette
def test_fetch_with_query():
    client = SongMetadataClient()

    metadata = client.fetch("Faint - Linkin Park")

    assert metadata is not None
    assert isinstance(metadata, SongMetadata)
    assert metadata.artist == "Linkin Park"
    assert metadata.name == "Faint"
    assert metadata.album_name == "Meteora"


@my_vcr.use_cassette
def test_fetch_raise_exception_if_bad_request():
    client = SongMetadataClient()

    try:
        metadata = client.fetch("foo bar baz azerazrqrsrtxv")
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


@my_vcr.use_cassette
def test_search():
    client = SongMetadataClient()
    limit = 10

    metadatas = client.search("faint - linkin park", limit)

    assert len(metadatas) >= limit

    first_metadata = metadatas[0]

    assert first_metadata.artist == "Linkin Park"
    assert first_metadata.name == "Faint"
    assert first_metadata.album_name == "Meteora 20th Anniversary Edition"
