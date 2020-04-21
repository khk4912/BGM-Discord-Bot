import logging
import discord

""" 봇 전체 사용 로거 """


class Logs:
    def __init__(self):
        pass

    def create_logger(self):

        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = logging.Formatter(
            "[%(asctime)s][%(name)s][%(levelname)s] %(message)s "
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        filehandler = logging.FileHandler(
            "Bot_Logs/{}.txt".format(self.__class__.__name__), "w"
        )
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        logger.addHandler(stream_handler)
        logger.info("{} Loaded.".format(self.__class__.__name__))
        return logger

    @classmethod
    def main_logger(cls):
        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s][%(name)s][%(levelname)s] %(message)s "
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        filehandler = logging.FileHandler(
            "Bot_Logs/{}.txt".format(cls.__name__), "w"
        )
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        logger.addHandler(stream_handler)
        return logger
