class Stack(object):
    def __init__(self):
        self.stack = []

    def push(self,val):
        self.stack.append(val)

    def is_empty(self):
        return self.size()==0

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.stack.pop()
    #取栈顶值
    def peak(self):
        if self.is_empty():
            return None
        else:
            return self.stack[-1]
    def size(self):
        return len(self.stack)
if __name__ == '__main__':
    stack = Stack()
    for i in range(5):
        stack.push(i)
    print(stack.is_empty())
    print(stack.size())
    for i in range(3):
        print(stack.pop())
    print(stack.size(),stack.peak())

