from typing import List
from taipan_di import PipelineLink
from mumee.data import SongMetadata, SearchMetadataCommand

__all__ = ["BaseMetadataExplorer"]


BaseMetadataExplorer = PipelineLink[SearchMetadataCommand, List[SongMetadata]]
