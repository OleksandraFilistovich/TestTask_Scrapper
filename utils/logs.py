from loguru import logger


def get_logger(name: str, rotation="5 MB") -> logger:
    a = logger.add(f'./logs/{name}.log', format="{time} {level} {name}:{function}:{line} {message}",
               level="ERROR", rotation=rotation, compression="zip")
    # logger.add(f'./logs/{name}.log', format="{time} {level} {name}:{function}:{line} {message}",
    #            level="DEBUG", rotation=rotation, compression="zip")
    return logger


if __name__ == '__main__':
    logger_ = get_logger('ggg')
    d = logger_.info('hello')
    print(d)
    