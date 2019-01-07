def partition(lst,l,r):
    x = lst[r]
    i = l - 1
   # q = r - 1
    for j in range(l,r):
        if lst[j]<=x:
            i += 1
            lst[j],lst[i] = lst[i],lst[j]
    lst[i+1],lst[r] = lst[r],lst[i+1]

    return i+1
def quick_sort(lst,l,r):
    if l < r:
        q = partition(lst,l,r)
        quick_sort(lst,0,q-1)
        quick_sort(lst,q+1,r)
if __name__ == '__main__':
    lst = [3,5,51,56,7,23,75,9,24,568,424]
    quick_sort(lst,0,10)
    print(lst)
