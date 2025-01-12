import logging 
from pathlib import Path
import datetime as dt 


def create_log_path(module_name : str)->str:

    """
    creates a log file path based on current date and provided module name. 

    Parameters : 
    
    - module_name (str) : The name of the log directory. 

    Returns : 
    - str : The complete path of the log file. 
    """

    root_path = Path(__file__).parent.parent

    log_dir_path = root_path / "logs"
    log_dir_path.mkdir(exist_ok= True)

    module_dir_path = log_dir_path / module_name 
    module_dir_path.mkdir(parents= True , exist_ok= True)

    current_date = dt.date.today()
    current_date_str = current_date.strftime("%d-%m-%Y") + ".log"
    log_file_path = module_dir_path / current_date_str
    return log_file_path


class CustomLogger:
    
    def __init__(self , logger_name , log_filename):

        """
        Initializes a custom logger with the specified name and log file.
        Parameters:
        - logger_name (str): Name of the logger.
        - log_filename (str): Path to the log file.
        """

        self.__logger = logging.getLogger(name = logger_name)
        self.__log_path = log_filename

        filehandler = logging.FileHandler(filename= log_filename , mode = 'a')

        time_format = '%d-%m-%Y %H:%M:%S'
        log_format = "%(asctime)s - %(levelname)s : %(message)s"

        formatter = logging.Formatter(fmt= log_format , datefmt=time_format)
        filehandler.setFormatter(fmt = formatter)

        self.__logger.addHandler(hdlr= filehandler)
    

    def get_log_path(self):
        """
        returns the log file path. 
        """

        return self.__log_path
    
    
    def get_logger(self):
        """
        returns the custom logger object
        """

        return self.__logger
    
    
    def set_log_level(self , level = logging.DEBUG):
        """
        Sets the log level for the logger.
        Parameters:
        - level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
        """
        logger = self.get_logger()
        logger.setLevel(level= level)


    def save_logs(self , msg , log_level = 'info'):
        """
        Saves logs to the specified log file with the given message and log level.
        Parameters:
        - msg (str): Log message.
        - log_level (str): Log level ('debug', 'info', 'warning', 'error', 'exception', 'critical').
        """

        logger = self.get_logger()
        
        if log_level == 'debug':
            logger.debug(msg=msg)
        elif log_level == 'info':
            logger.info(msg=msg)
        elif log_level == 'warning':
            logger.warning(msg=msg)
        elif log_level == 'error':
            logger.error(msg=msg)
        elif log_level == 'exception':
            logger.exception(msg=msg)
        elif log_level == 'critical':
            logger.critical(msg=msg)

if __name__ == "__main__":
    
    logger = CustomLogger(logger_name= "my_logger" , log_filename= create_log_path("test"))
    logger.set_log_level()
    logger.save_logs(msg = "I am gonna die , please help me , i am under the water" , log_level= "critical")