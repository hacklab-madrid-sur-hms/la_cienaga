from la_cienaga.core.config import Config
import logging as logger

logger.basicConfig(level=logger.INFO, format='%(asctime)s :: %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# leemos la config general
settings = Config()
logger.info('Leídas settings: {}'.format(settings))
