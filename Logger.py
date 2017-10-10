
import logging
import logging.config

__all__ = ["dbgprint", "logprint"]

logging.config.fileConfig("logging.conf")
dbgprint = logging.getLogger("dbgprint")
logprint = logging.getLogger("logprint")

class Logger():
    def __init__(self):
        pass
    
    



            
            
            
            
