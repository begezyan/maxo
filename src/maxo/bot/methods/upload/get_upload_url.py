from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.enums.upload_type import UploadType
from maxo.types.upload_endpoint import UploadEndpoint


class GetUploadUrl(MaxoMethod[UploadEndpoint]):
    """
    Загрузка файлов

    Метод возвращает URL для последующей загрузки файла

    > Параметр `type=photo` больше не поддерживается. Если вы использовали `type=photo` в ранее созданных интеграциях - замените его на `type=image`

    #### Ограничения при загрузке файлов
    - Максимальный размер файла: 4 ГБ
    - Можно загружать только один файл за раз

    #### Пример получения URL для загрузки

    ```bash
    curl -X POST "https://platform-api.max.ru/uploads?type=file" \
      -H "Authorization: {access_token}"
    ```

    #### Файлы по полученному URL можно загрузить двумя способами

    - **Resumable upload** - надёжный способ, если заголовок `Content-Type` не равен `multipart/form-data`. Этот способ позволяет загружать файл частями и возобновить загрузку с последней успешно загруженной части в случае ошибок. 
     Пример загрузки файла по полученному URL:

    ```bash
    curl -X POST "%UPLOAD_URL%" \
      -H "Authorization: {access_token}" \
      -F "data=@example.mp4"
    ```

    - **Multipart upload** - более простой, но менее надёжный способ. В этом случае используется заголовок `Content-Type: multipart/form-data`. Файл отправляется целиком одним запросом. Если загрузка прервётся, невозможно её возобновить - придётся начать заново. 
     Пример использования cURL для загрузки файла:

    ```shell
    curl -i -X POST \
      -H "Content-Type: multipart/form-data" \
      -F "data=@movie.pdf" "%UPLOAD_URL%"
    ```

    где `%UPLOAD_URL%` - это URL из результата метода в примере cURL запроса

    **Особенности загрузки видео и аудио:**

    - Когда получаем ссылку на загрузку видео или аудио (`POST /uploads` с `type` = `video` или `type` = `audio`), вместе с `url` в ответе приходит `token`, который нужно использовать в сообщении (когда формируете `body` с `attachments`) в [`POST /messages`](https://dev.max.ru/docs-api/methods/POST/messages)
    - После загрузки видео или аудио (по `url` из шага выше) сервер возвращает `retval`
    - C этого момента можно использовать `token`, чтобы прикреплять вложение в сообщение бота

    **Особенности загрузки изображений и файлов:**

    - Для`type` = `file`: `token` возвращается в ответе на загрузку файла
    - Для`type` = `image`:
        - `token` возвращается в ответе на загрузку файла
        - `token` содержится в URL, возвращаемом в методе для загрузки файла

    ## Прикрепление медиа
    Процесс прикрепления медиафайлов к сообщениям состоит из трёх шагов:

    #### 1. Получение URL для загрузки медиафайлов

    Отправьте запрос:

    ```bash
    curl -X POST "https://platform-api.max.ru/uploads?type=video" \
      -H "Authorization: {access_token}"
    ```

    где `{type}` - тип загружаемого файла:
    - `file` - произвольный файл
    - `image` - изображение
    - `video` / `audio` - видео или аудио

    Ответ:
    ```json
    {
        "url": "https://<upload-host>/upload.do?..."
    }
    ```

     > Обратите внимание:  домен в `url` зависит от типа файла. Это ожидаемое поведение:
    `file` → `https://fu.oneme.ru`
    `image` → `https://iu.oneme.ru`
    `video` / `audio` → `https://vu.okcdn.ru`

    #### 2. Загрузка медиафайла

    Используйте полученный `url` без изменений:

    ```bash
    curl -X POST \
      -H "Content-Type: multipart/form-data" \
      -F "data=@movie.mp4" \
      "{url}"
    ```

    Ответ:
    ```json
    {
        "token": "_3Rarhcf1PtlMXy8jpgie8Ai_KARnVFYNQTtmIRWNh4"
    }
    ```

    #### 3. Создание вложения 

     После успешной загрузки получите JSON-объект в ответе. Используйте этот объект для создания вложения. Структура вложения:
    - `type`: тип медиа, например `"video"`
    - `payload`: JSON-объект, который вы получили.

    Отправьте сообщение с вложением:

    ```json
    {
        "text": "Message with video",
        "attachments": [
            {
                "type": "video",
                "payload": {
                    "token": "_3Rarhcf1PtlMXy8jpgie8Ai_KARnVFYNQTtmIRWNh4"
                }
            }
        ]
    }
    ```

    ## Обработка файлов

    После успешной загрузки сервер обрабатывает файл. Файлы от нескольких мегабайт обрабатываются дольше

    > Для стабильной работы сервисов MAX убедитесь, что максимальное количество запросов в секунду на platform-api.max.ru - 30 rps 

    Если отправить сообщение с вложением сразу после загрузки, может возникнуть ошибка:

    ```json
    {
      "code": "attachment.not.ready",
      "message": "Key: errors.process.attachment.file.not.processed"
    }
    ```

    **Как избежать ошибки:**
    - После загрузки файла сделайте паузу перед отправкой сообщения
    - Если отправка не удалась, повторите попытку через некоторое время. Увеличивайте интервал с каждой попыткой
    - Загружайте часто используемые файлы заранее и переиспользуйте токен

    Args:
        type: Тип загружаемого файла. Возможные значения: `"image"`, `"video"`, `"audio"`, `"file"`

    Источник: https://dev.max.ru/docs-api/methods/POST/uploads
    """

    __url__ = "uploads"
    __method__ = "post"

    type: Query[UploadType]
    """Тип загружаемого файла. Возможные значения: `"image"`, `"video"`, `"audio"`, `"file"`"""
