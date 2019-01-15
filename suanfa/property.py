import time
from threading import Thread


def func(f):
    def func2(*arg,**keyword):
        g = f(*arg,**keyword)
        gg = next(g)
        def inner(ggg):
            ggg = next(gg)
            try:
                g.send(ggg)
            except:
                pass
        thread = Thread(target=inner,args=[gg,])
        thread.start()

    return func2
def follow_to():
    print('start follow_to')
    time.sleep(5)
    print('end follow_to')
    yield 'haha'
@func
def rep_a():
    print('start rep_a')

    s = yield follow_to()
    time.sleep(5)
    print(s)
    print('end rep_a')

def rep_b():
    print('start rep_b')
    time.sleep(2)
    print('end rep_b')


if __name__=='__main__':
    rep_a()
    rep_b()
    while 1:
        pass
