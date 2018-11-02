from auditexport import cli
import logging

ROOT_LOGGER = 'auditexport'

if __name__ == '__main__':
    # Set default logger
    logger = logging.getLogger(ROOT_LOGGER)
    logger.setLevel(logging.INFO)
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.WARNING)

    streamformat = logging.Formatter(
        '%(name)s - [%(levelname)s] - %(message)s')
    streamhandler.setFormatter(streamformat)

    logger.addHandler(streamhandler)

    # Main application
    cli.main()
