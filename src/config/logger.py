# create a logger class for the phonenix agent that can be used throughout the project
# its should show the name of the file and the line number of the log and time of the log

import logging

logger = logging.getLogger("phonenix-agent")
logger.setLevel(logging.INFO)

class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        
    def get_logger(self):
        return self.logger
