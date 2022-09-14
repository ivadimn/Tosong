commands = {"/high"
            "/help": "Помощь;",
            "/values": "Список всех возможных валют;",
            "<имя валюты> <в какую валюту перевести> <количество переводимой валюты>": "запрос суммы."}


class MsgsRu:
    WELCOME = "Привет {0}, добро пожаловать в бот, получающий звуковую дорожку из видео YouTube"
    COMMANDS = {"/high": "Скачать видео в высоком разрешении",
                "/audio": "Скачать аудио дорожку видео",
                "/help": "Показать подсказку" }
    AUDIO_MODE = "Для получения аудио дорожки из видео, введите URL видео на YouTube..."
    ERROR = "Произошла ошибка: {0}"
    REPEAT = "Повторить попытку?(да/нет)"
    REPEAT_INPUT = "Повторить ввод URL?(да/нет)"
    BAD_URL = "Введена не корректная ссылка...{0}"
    SELECT_COMMAND = "Выберите команду..."
    PROGRESS = "Идёт загрузка..."
    COMPLETE = "Загрузка завершена, ожидаем файл..."
    STOP_ERROR = "При загрузке файла произошла ошибка."
    ANOTHER_ATTEMPT = "Ещё одна попытка."


class MsgsEn:
    WELCOME = "Hello {0}, welcome to get audio from YouTube video bot"
    COMMANDS = {"/high": "Dwonload video in highest resolution",
                "/audio": "Dwonload audio track from video",
                "/help": "Show help"}
    AUDIO_MODE = "To get the audio track from a video, enter the YouTube video URL..."
    ERROR = "An error has occurred: {0}"
    REPEAT = "To retry?(yes/no)"
    REPEAT_INPUT = "Do you will retry input URL?(yes/no)"
    BAD_URL = "Bad URL address was entered...{0}"
    SELECT_COMMAND = "Select command..."
    PROGRESS = "Downloading in progress..."
    COMPLETE = "Download completed, waiting for the file..."
    STOP_ERROR = "An error occurred while downloading the file"
    ANOTHER_ATTEMPT = "Another attempt."


msgs = {"ru": MsgsRu, "en": MsgsEn}
