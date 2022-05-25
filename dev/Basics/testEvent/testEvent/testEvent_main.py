# https://udemyfun.com/python-thread-event/

import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')



def thread( event ):
    logging.debug('start3')
    time.sleep(2)
    logging.debug('end3')
    event.set()# wait()から先に進んでもいいですよフラグ



if __name__ == '__main__':
    event = threading.Event()
    #event.clear()# wait()で待ちなさいフラグ

    t = threading.Thread( target=thread, args=(event, ) )
    t.start()

    event.wait()# スレッド側でイベントセットされるまで待つ
    print( "continue main..." )
