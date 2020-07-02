from .logger import Logger


class NopLogger(Logger):
    def log(self, type: str, msg: dict) -> None:
        pass
