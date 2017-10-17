import logging

class LoggingUtils:

    @staticmethod
    def initialize_logger(name, level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        ch = logging.StreamHandler()
        ch.setLevel(level)

        # e.g. 2017-10-16 19:09:48,098 [imgur_utils.py:43 _get_local_time()] ERROR: invalid input.
        formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)d %(funcName)s()] %(levelname)s: %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)
