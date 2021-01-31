import logging
from src.constants import Files


logging.basicConfig(filename=Files.LOG_FILE,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def info(s):
    logging.info(s)
