"""class and methods for logs handling."""

import logging
import google.cloud.logging_v2

logging_client = google.cloud.logging_v2.Client()
logging_client.get_default_handler()
logging_client.setup_logging()

logging.basicConfig(level=logging.INFO)


class Logger():
  """class def handling logs."""

  @staticmethod
  def info(message):
    """Display info logs."""
    logging.info(message)

  @staticmethod
  def warning(message):
    """Display warning logs."""
    logging.warning(message)

  @staticmethod
  def error(message):
    """Display error logs."""
    logging.error(message)
