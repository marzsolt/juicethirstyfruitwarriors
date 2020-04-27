import logging
import src.utils.awesome_logging as al

al.setup_logger()
# Create a custom logger
logger = logging.getLogger('Domi.hihi')

logger.warning('This is a warning')
logger.error('This is an error')