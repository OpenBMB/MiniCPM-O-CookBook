import logging
import sys
import os

# setup root logger
def setup_root_logger(log_level=logging.INFO, dist_rank=0, local_dir=''):
    """
        log_level: logging level
        dist_rank: process rank for distributed training
        local_dir: local log path, default None
    """
    logger = logging.getLogger() # setup root logger for all
    for handler in logger.handlers:
        logger.removeHandler(handler)
    # create formatter
    fmt = '[%(asctime)s] (%(filename)s %(lineno)d): %(levelname)s %(message)s'
    #color_fmt = colored('[%(asctime)s]', 'green') + \
    #        colored('(%(filename)s %(lineno)d)', 'yellow') + ': %(levelname)s %(message)s'

    # create console handlers for master process
    if dist_rank == 0:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(console_handler)

    # create file handlers
    if local_dir:
        os.makedirs(local_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(local_dir, f'log_rank{dist_rank}.log'), mode='a')
        file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(file_handler)

    logger.setLevel(log_level)
