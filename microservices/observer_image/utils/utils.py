from pymongo.change_stream import CollectionChangeStream
from multiprocessing import Process

class Utils:
    __MONGO_NEXT_RESULT = None

    def __call_mongo_watcher(self,cursor: CollectionChangeStream):
        self.__MONGO_NEXT_RESULT = cursor.next()

    def call_cursor_with_timeout(self,cursor: CollectionChangeStream,
                                 timeout: int = 0):

        process = Process(target=self.__call_mongo_watcher(cursor),
                          name='call_mongo_watcher')
        process.start()

        if timeout <= 0:
            process.join()
        else:
            process.join(timeout=timeout)

        if process.exitcode is None:
            process.terminate()
            return None

        result = self.__MONGO_NEXT_RESULT
        self.__MONGO_NEXT_RESULT = None

        return result
