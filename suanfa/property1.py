from threading import Thread
import time


def func(f):
    def wraper(*args,**keyargs):
        ger = f(*args,**keyargs)
        r = next(ger)
        def func1(r):
            s = next(r)
            try:
                ger.send(s)
            except:
                pass
        thread = Thread(target=func1,args=[r,])
        thread.start()
        return thread
    return wraper




def fallow():
    print('开始执行IO操作')
    time.sleep(2)
    print('执行IO结束')
    yield 'hahah'


@func
def rap_a():
    print('开始执行rap_a')
    s = yield fallow()
    time.sleep(5)
    print(s)
    print('执行结束rap_a')


def rap_b():
    print('开始执行rap_b')
    time.sleep(2)
    print('执行结束rap_b')

if __name__=='__main__':
    rap_a()
    rap_b()
    while True:
        pass






