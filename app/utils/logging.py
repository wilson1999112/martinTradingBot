""" Logging, TODO"""
from fastapi.logger import logger
import logging
from binance.lib.utils import config_logging
config_logging(logging, logging.INFO)