from enum import StrEnum


class UploadType(StrEnum):
    """
    Тип загружаемого файла

    Поддерживаемые форматы:
    - `image`: JPG, JPEG, PNG, GIF, TIFF, BMP, HEIC
    - `video`: MP4, MOV, MKV, WEBM, MATROSKA
    - `audio`: MP3, WAV, M4A и другие
    - `file`: файл для загрузки. Поддерживаются распространённые форматы (например, .txt, .doc и другие). В случае передачи неподдерживаемого типа файла будет возвращена ошибка  `File extension is forbidden`

    > Значение `photo` больше не поддерживается. Если вы использовали `type=photo` в ранее созданных интеграциях - замените его на `type=image`
    """

    AUDIO = "audio"
    FILE = "file"
    IMAGE = "image"
    VIDEO = "video"
