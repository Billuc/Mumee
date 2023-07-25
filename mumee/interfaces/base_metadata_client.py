from typing import Union
from taipan_di import PipelineLink
from mumee.data import SongMetadata, PlaylistMetadata

__all__ = ["BaseMetadataClient"]


BaseMetadataClient = PipelineLink[str, Union[SongMetadata, PlaylistMetadata]]
