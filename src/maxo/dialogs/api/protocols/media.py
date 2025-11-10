from abc import abstractmethod
from typing import Optional, Protocol

from maxo.dialogs.api.entities import MediaId
from maxo.enums import AttachmentType


class MediaIdStorageProtocol(Protocol):
    @abstractmethod
    async def get_media_id(
        self,
        path: Optional[str],
        url: Optional[str],
        type: AttachmentType,
    ) -> Optional[MediaId]:
        raise NotImplementedError

    @abstractmethod
    async def save_media_id(
        self,
        path: Optional[str],
        url: Optional[str],
        type: AttachmentType,
        media_id: MediaId,
    ) -> None:
        raise NotImplementedError
