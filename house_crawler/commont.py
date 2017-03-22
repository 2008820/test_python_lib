import time
import traceback
import re
def try_number(num, second):
    def _func(func):
        def __func(*args, **kwargs):
            loop = 0
            while 1:
                loop += 1
                try:
                    return func(*args, **kwargs)
                except:
                    print traceback.print_exc()
                    time.sleep(second)
                    if loop == num:
                        return ''
                        pass

        return __func

    return _func
