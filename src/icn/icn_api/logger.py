import logging
import os
import sys

logger = None


def initialize_logs(boot_logger):
    try:
        os.makedirs('logs', exist_ok=True)
        boot_logger.info('logs startup successful.')
    except Exception as e:
        boot_logger.error('logs directory could not be created. {}'.format(e))
        pass


def build_console_handler():
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.setFormatter(formatter)
    return handler_console


if __name__ == '__main__':
    pass
else:
    # Build the boot logger
    logger = logging.getLogger('icn_api_boot')

    # Set log level
    logger.setLevel(logging.INFO)

    # Build handler
    handler_console = build_console_handler()

    # Append console handler
    logger.addHandler(handler_console)

    # Create log directory, it needs to exist to dump APP logs.
    initialize_logs(logger)


