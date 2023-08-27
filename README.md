# Mumee

**Get metadata about your favorite songs and playlists !**  
Mumee stands for *MUsic MEtadata Explorer*

## Features

- Automatic metadata fetching from different services
  - Currently supported : Spotify, Youtube Music
- Metadata fetching from an URL or a query
- Supports playlist URLs
- Easy to use, straightforward interface
- Possible to use via DI integration

## Installation

### Pip

```
pip install mumee
```

### Poetry

[Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool. I actually use it for this project.

```
poetry add mumee
```

## Usage

There are 2 ways to use this library : using the `SongMetadataClient` object or via the DI.

### Using SongMetadataClient

The library exposes the `SongMetadataClient` class. This class has 2 methods : `fetch` and `search`.

The `fetch` method fetches the metadata corresponding to the request you give it, whether it is an URL or a query. It returns the result as a `SongMetadata` object or a `PlaylistMetadata` object.

**Example :**

```python
from mumee import SongMetadataClient

client = SongMetadataClient()
result = client.fetch("https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr")

title = result.title # Faint
artists = result.artists # ['Linkin Park']
```

The `search` method expects a query (e.g.: {title} - {artists}) and a limit corresponding to the number of results you want. It returns a list of `SongMetadata` objects that fit closest to the query that was given. This list is sorted by closest fit per client.

**Example :**

```python
from mumee import SongMetadataClient

client = SongMetadataClient()
results = client.search("in the end - linkin park")

title = results[0].title # In The End
artists = results[0].artists # ['Linkin Park']
```

### Using DI

The library also exposes the `BaseMetadataClient` and `BaseMetadataExplorer` interfaces and a `add_mumee` function for [Taipan-DI](https://github.com/Billuc/Taipan-DI).

In this function, the clients and explorers are registered as a Pipeline. All you need to do is to resolve the pipelines and execute it.

**Example 1 :**

```python
from mumee import BaseMetadataClient, add_mumee
from taipan_di import DependencyCollection

services = DependencyCollection()
add_mumee(services)

provider = services.build()
client = provider.resolve(BaseMetadataClient)

result = client.exec("https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr")
title = result.title # Faint
```

**Example 2 :**

```python
from mumee import BaseMetadataExplorer, add_mumee
from taipan_di import DependencyCollection

services = DependencyCollection()
add_mumee(services)

provider = services.build()
explorer = provider.resolve(BaseMetadataExplorer)

command = SearchMetadataCommand("in the end - linkin park")
results = explorer.exec(command)
title = results[0].title # In The End
```

## Inspirations

This library is partially based on spotDL's [spotify-downloader](https://github.com/spotDL/spotify-downloader).

## TODO

This library isn't stable yet and a lot of things can still be improved.
If there is something you want to see added or if something does not work as you want it to, feel free to open an issue.

Here is a list of features I have in mind and will be working on :

- Support for Amazon Music
- More metadata in the SongMetadata class
- Re-sort explorer results
