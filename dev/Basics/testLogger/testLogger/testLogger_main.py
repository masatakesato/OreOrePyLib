import traceback
from oreorepylib.logger.logger import Logger



if __name__ == "__main__":

    logger = Logger(__name__)
    logger.info('info_')

    try:
       cmds.polySphere()   
       a = 10 / 0

    except Exception as e:
       logger.critical( traceback.format_exc() )

    logger.close()