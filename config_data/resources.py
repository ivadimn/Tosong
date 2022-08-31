commands = {"/"
            "/help": "Помощь;",
            "/values": "Список всех возможных валют;",
            "<имя валюты> <в какую валюту перевести> <количество переводимой валюты>": "запрос суммы."}

class MsgsRu:
    WELCOME = "Привет {0}, добро пожаловать в бот, получающий звуковую дорожку из видео YouTube"
    COMMANDS = {"/high": "Скачать видео в высоком разрешении",
                "/audio": "Скачать аудио дорожку видео",
                "/help": "Показать подсказку" }
    AUDIO_MODE = "Для получения аудио дорожки из видео введите URL видео на YouTube..."

class MsgsEn:
    WELCOME = "Hello {0}, welcome to get audio from YouTube video bot"
    COMMANDS = {"/high": "Dwonload video in highest resolution",
                "/audio": "Dwonload audio track from video",
                "/help": "Show help"}
    AUDIO_MODE = "To get the audio track from a video, enter the YouTube video URL..."


msgs = {"ru": MsgsRu, "en": MsgsEn}
