from taipan_di import PipelineLink
from song_metadata_client.classes import SongMetadata

__all__ = ["BaseMetadataClient"]


BaseMetadataClient = PipelineLink[str, SongMetadata]
