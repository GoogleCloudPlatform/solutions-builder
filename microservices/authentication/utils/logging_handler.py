"""Utility methods for logging"""
import logging

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s", level=logging.DEBUG)


class Logger():
  """Class def handling logging"""

  @staticmethod
  def info(message):
    """Logs info message"""
    logging.info(message)

  @staticmethod
  def warning(message):
    """Logs warning message"""
    logging.warning(message)

  @staticmethod
  def debug(message):
    """Logs debug message"""
    logging.debug(message)

  @staticmethod
  def error(message):
    """Logs error message"""
    logging.error(message)
