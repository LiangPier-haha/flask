def insert_sort(arr):
    for i in range(1,len(arr)):
        key = arr[i]
        j = i - 1
        while j>=0 and arr[j]>key:
            arr[j+1] = arr[j]
            j -= 1

        arr[j+1] = key

    return arr

if __name__=='__main__':
    arr = [4,7,2,9,3,5,8,1]
    print(insert_sort(arr))


