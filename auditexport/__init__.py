import logging

# Set up root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)

streamformat = logging.Formatter(
    '%(name)s - [%(levelname)s] - %(message)s')
streamhandler.setFormatter(streamformat)

logger.addHandler(streamhandler)
