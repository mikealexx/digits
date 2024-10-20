import logging

class LoggerSingleton:
    '''
    Singleton class for logging.
    '''
    _instance = None

    @staticmethod
    def get_logger():
        '''
        Get the logger instance.
        '''

        if LoggerSingleton._instance is None:
            LoggerSingleton._instance = LoggerSingleton._create_logger()
        return LoggerSingleton._instance
    
    @staticmethod
    def _create_logger():
        '''
        Create the logger instance.
        '''

        logger = logging.getLogger("digits")

        # Set the log level
        logger.setLevel(logging.INFO)

        # Create handlers: console and file handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("logs/digits.log")

        # Set log level for the handlers
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.INFO)

        # Create formatters and add them to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(tag)s] - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger