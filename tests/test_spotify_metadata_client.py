from song_metadata_client.classes import SpotifyOptions, SpotifyMetadataClient
from tests.my_vcr import generate_vcr

my_vcr = generate_vcr("test_spotify_metadata_client")

def test_init_client():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)
    

@my_vcr.use_cassette()
def test_get_from_url():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)
    
    metadata = client.get_from_url("https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr?si=5cc9c24b381446f7")

    assert metadata is not None
    assert metadata.artist == "Linkin Park"
    assert metadata.name == "Faint"
    assert metadata.album_name == "Meteora (Bonus Edition)"
    

@my_vcr.use_cassette()
def test_search():
    options = SpotifyOptions()
    client = SpotifyMetadataClient(options)
    
    metadata = client.search("Faint", "Linkin Park")

    assert metadata is not None
    assert metadata.artist == "Linkin Park"
    assert metadata.name == "Faint"
    assert metadata.album_name == "Meteora"
    