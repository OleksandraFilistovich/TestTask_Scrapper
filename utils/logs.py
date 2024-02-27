from loguru import logger
from loguru._logger import Logger


def get_logger(name: str, rotation="5 MB") -> Logger:
    a = logger.add(f'./logs/{name}.log', format="{time} {level} {name}:{function}:{line} {message}",
               level="ERROR", rotation=rotation, compression="zip")
    return logger


if __name__ == '__main__':
    logger_ = get_logger('orchestrator')
    d = logger_.info('module launched')

    logger_2 = get_logger('worker')
    logger_2.info('worker launched')
    logger_2.warning('worker launched')
    logger_2.error('worker launched')
    logger_2.success('worker launched')
