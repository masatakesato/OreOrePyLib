from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG


class Logger:

    def __init__( self, name=__name__, filepath='D:/oreorelog.txt' ):
        self.logger = getLogger(name)
        self.logger.propagate = False
        self.logger.setLevel(DEBUG)

        if( not len(self.logger.handlers) ):
            formatter = Formatter( '[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s]\n %(message)s\n' )

            # stdout
            handler = StreamHandler()
            handler.setLevel(DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            # file
            handler = handlers.RotatingFileHandler( filename = filepath, maxBytes = 1048576, backupCount = 3 )
            handler.setLevel(DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        

    def close( self ):
        for handler in self.logger.handlers:
            handler.close()
        

    def debug( self, msg ):
        self.logger.debug(msg)


    def info( self, msg ):
        self.logger.info(msg)


    def warn( self, msg ):
        self.logger.error(msg)


    def critical( self, msg ):
        self.logger.critical(msg)
