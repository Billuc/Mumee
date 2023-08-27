from mumee.classes import YTMusicMetadataClient
from mumee.errors import MetadataClientError
from tests.my_vcr import generate_vcr

my_vcr = generate_vcr("test_ytmusic_metadata_client")


def test_init_client():
    client = YTMusicMetadataClient()


@my_vcr.use_cassette
def test_get_track():
    client = YTMusicMetadataClient()

    metadata = client.get_track(
        "https://music.youtube.com/watch?v=dLohoBAnoTk&feature=share"
    )

    assert metadata is not None
    assert metadata.album_artist == "Currents"
    assert metadata.album_name == "The Death We Seek"
    assert metadata.artist == "Currents"
    assert metadata.artists == ["Currents"]
    assert (
        metadata.cover_url
        == "https://lh3.googleusercontent.com/lIpQFd_pEFcvBIIMDUosKUVbT3bl1JFZ9F-nc2Tj6pqebAMLrOgq8a2Xe9c85-XOmvGYgQIwhroRmtBb=w544-h544-l90-rj"
    )
    assert metadata.date == None
    assert metadata.disc_count == None
    assert metadata.disc_number == None
    assert metadata.duration == 219
    assert metadata.explicit == False
    assert metadata.genres == []
    assert metadata.id == "dLohoBAnoTk"
    assert metadata.is_song == True
    assert metadata.name == "Gone Astray"
    assert metadata.track_count == 10
    assert metadata.track_number == 7
    assert metadata.url == "https://music.youtube.com/watch?v=dLohoBAnoTk"
    assert metadata.year == 2023


def test_get_track_error_if_music_youtube_not_in_url():
    client = YTMusicMetadataClient()

    try:
        client.get_track(
            "https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr?si=5cc9c24b381446f7"
        )
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


def test_get_track_error_if_watch_not_in_url():
    client = YTMusicMetadataClient()

    try:
        client.get_track(
            "https://music.youtube.com/playlist?list=PLNvqJjX5l6qXLjKMC_rTgwcyw4VGKP2lO"
        )
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


@my_vcr.use_cassette
def test_get_track_error_if_wrong_url():
    client = YTMusicMetadataClient()

    try:
        client.get_track(
            "https://music.youtube.com/watch?v=dLohoBAnoTl&feature=share"
        )  # this url does not exist
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


@my_vcr.use_cassette
def test_get_playlist():
    client = YTMusicMetadataClient()

    metadata = client.get_playlist(
        "https://music.youtube.com/playlist?list=RDCLAK5uy_keb_mIiClglpMd5ycINvnTwCkoIu5Ce3k"
    )

    assert metadata is not None
    assert metadata.name == "'00s Rock"
    assert metadata.author == "YouTube Music"
    assert metadata.description.startswith("New millennium rock and roll!")
    assert any(track.name == "Numb" for track in metadata.tracks)


def test_get_playlist_error_if_music_youtube_not_in_url():
    client = YTMusicMetadataClient()

    try:
        client.get_playlist(
            "https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr?si=5cc9c24b381446f7"
        )
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


def test_get_playlist_error_if_playlist_not_in_url():
    client = YTMusicMetadataClient()

    try:
        client.get_playlist("https://music.youtube.com/search?q=00s")
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False


@my_vcr.use_cassette
def test_get_playlist_error_if_wrong_url():
    client = YTMusicMetadataClient()

    try:
        client.get_playlist(
            "https://music.youtube.com/playlist?list=RDCLAK5uy_keb_mIiClglpMd5ycINvnTwCkoIu5Ce3l"
        )
        assert False
    except Exception as ex:
        assert True


@my_vcr.use_cassette
def test_search():
    client = YTMusicMetadataClient()
    limit = 3

    metadatas = client.search("Faint - Linkin Park", limit, True)

    assert metadatas is not None
    assert len(metadatas) == limit

    metadata = metadatas[0]

    assert metadata.artist == "Linkin Park"
    assert metadata.name == "Faint"
    assert metadata.album_name == "Meteora (Bonus Edition)"


@my_vcr.use_cassette
def test_search_error_if_bad_results():
    client = YTMusicMetadataClient()

    try:
        client.search("foo bar baz", 1, True)
        assert False
    except MetadataClientError as ex:
        assert True
    except:
        assert False
