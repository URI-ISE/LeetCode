import threading

class FooBar(object):
    def __init__(self, n):
        self.n = n
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()
        self.lock2.acquire()

    def foo(self, printFoo):
        """
        :type printFoo: method
        :rtype: void
        """
        for i in xrange(self.n):
            # printFoo() outputs "foo". Do not change or remove this line.
            self.lock2.release()
            printFoo()
            self.lock1.acquire()


    def bar(self, printBar):
        """
        :type printBar: method
        :rtype: void
        """
        for i in xrange(self.n):            
            # printBar() outputs "bar". Do not change or remove this line.
            self.lock1.release()
            printBar()
            self.lock2.acquire()