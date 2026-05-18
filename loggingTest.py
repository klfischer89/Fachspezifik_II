import logging

# monitoring the process. level for logging: DEBUG, INFO, WARNING, ERROR, CRITICAL, using INFO
logging.basicConfig(filename="test.log", level=logging.INFO, format="%(asctime) s - %(message) s")

try:
    result = 10/0
except ZeroDivisionError as e:
    logging.error("Fehler aufgetreten: %s", e)