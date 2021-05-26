import logging
import os
import sys
from colorlog import ColoredFormatter

logger = None


def initialize_logs(logger_name):
    boot_logger = build_boot_logger('{}_boot'.format(logger_name))
    try:
        os.makedirs('logs', exist_ok=True)
        if not os.path.exists('./logs/{}.log'.format(logger_name)):
            icn_log = open('./logs/{}.log'.format(logger_name), mode='w')
        boot_logger.debug('logs startup successful.')
    except Exception as e:
        boot_logger.error('logs directory could not be created. {}'.format(e))
        pass


def build_boot_logger(logger_name):
    handler_console = build_console_handler()

    boot_logger = logging.getLogger(logger_name)
    boot_logger.setLevel(logging.DEBUG)
    boot_logger.addHandler(handler_console)
    return boot_logger


def build_console_handler():
    formatter = ColoredFormatter('%(white)s%(name)s%(log_color)s - %(asctime)s - [%(levelname)s] - %(message)s')
    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.setLevel(logging.DEBUG)
    handler_console.setFormatter(formatter)
    return handler_console


def build_app_logger(logger_name):
    handler_console = build_console_handler()
    handler_file = build_file_handler(logger_name)

    app_logger = logging.getLogger(logger_name)
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(handler_console)
    app_logger.addHandler(handler_file)
    return app_logger


def build_file_handler(logger_name):
    formatter = ColoredFormatter('%(white)s%(name)s%(log_color)s - %(asctime)s - [%(levelname)s] - %(message)s')
    handler_file = logging.FileHandler(filename='./logs/{}.log'.format(logger_name), mode='a')
    handler_file.setLevel(logging.DEBUG)
    handler_file.setFormatter(formatter)
    return handler_file


if __name__ == '__main__':
    pass
else:
    initialize_logs('icn')
    logger = build_app_logger('icn')




