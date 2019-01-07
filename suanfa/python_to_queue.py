class Python_to_queue():
    def __init__(self):
        self.queue = []

    def enqueue(self,n):
        self.queue.append(n)

    def dequeue(self):
        if not self.queue:
            return None
        else:
            return self.queue.pop()
    def size(self):
        return len(self.queue)

    def is_empty(self):
        if not self.queue:
            return True
        else:
            return False

if __name__=='__main__':
    queue = Python_to_queue()
    for i in range(5):
        queue.enqueue(i)
    print(queue.size())
    for i in range(3):
       print(queue.dequeue(),i)
    print(queue.is_empty(),queue.size())


