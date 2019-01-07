def quick_sort(lst,l,r):
    if l==r:
        return
    x = l
    i = r
    temp = lst[x]

    if l>r:
        return
    while(x<i):
        while(i>x and temp<=lst[i]):
            i -= 1
        if i>x:
            lst[x] = lst[i]
        while(x<i and lst[x]<=temp):
            x += 1
        if x<i:
            lst[i] = lst[x]
    lst[x] = temp
    #print(x,lst[x])
    if l < r:
        quick_sort(lst,0,x-1)
        quick_sort(lst,x+1,r)


if __name__ == '__main__':
    lst = [3,5,51,56,7,23,75,9,24,568,424]
    num = len(lst)
    #try:
    quick_sort(lst,0,num-1)
    #except Exception as e:
     #   pass
    print(lst)
