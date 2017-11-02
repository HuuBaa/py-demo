# 冒泡排序:
def bubbleSort(arr):
    length=len(arr)
    for i in range(length):
        for j in range(length-i-1):
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
    return arr

L1=[0,9,8,7,6,5,4,3,2,1]

print('bubbleSort:%s'%bubbleSort(L1))

#选择排序
def selectSort(arr):
    length=len(arr)
    for i in range(length):
        min_index=i
        for j in range(i+1,length):
            if arr[j]<arr[min_index]:
                min_index=j
        arr[i],arr[min_index]=arr[min_index],arr[i]
    return arr
L7=[0,9,8,7,6,5,4,3,2,1]
print('selectSort:%s'%selectSort(L7))

#快速排序，分治，递归
def quickSort(arr):
    if len(arr)<2:
        return arr
    flag=arr[0]
    LL=[x for x in arr if x < flag]
    RL=[x for x in arr if x > flag]
    return quickSort(LL)+[x for x in arr if x == flag]+quickSort(RL)

L2=[0,9,8,7,6,5,4,3,2,1]
print('quickSort:%s'%quickSort(L2))

# 直接插入排序
# arr[0]到arr[i-1]已经有序，arr[i]是待插入的数，
# 遍历位置0-(i-1)的数与arr[i]比大小
# arr[i]插入到第一个比它大的数前面
def insertSort(arr):
    length=len(arr)
    for i in range(1,length):
        for j in range(i):
            if arr[i]<arr[j]:
                arr.insert(j,arr[i])
                arr.pop(i+1)
    return arr

def insertsort(arrs):
    # 插入排序
    count = len(arrs)
    for i in range(1, count):
        key = arrs[i]
        j = i - 1
        while j >= 0:
            if arrs[j] > key:
                arrs[j + 1] = arrs[j]
                arrs[j] = key               
            j -= 1               
    return arrs

L3=[0,9,8,7,6,5,4,3,2,1]
L4=[0,9,8,7,6,5,4,3,2,1]
print('insertSort:%s'%insertSort(L3))
print('insertsort:%s'%insertsort(L4))


#希尔排序
def shellSort(arr):
    length=len(arr)
    gap=length//2
    while gap>0:
        #插入排序
        for i in range(gap,length):
            key=arr[i]
            j=i-gap
            while j>=0:
                if key<arr[j]:
                    arr[j+gap]=arr[j]
                    arr[j]=key
                j-=gap
        gap=gap//2
    return arr

L5=[0,9,8,7,6,5,4,3,2,1]
print('shellSort:%s'%shellSort(L5))    


#归并排序
def merge(l,r):
    arr=[]
    while l and r:        
        arr.append(l.pop(0) if l[0]<=r[0] else r.pop(0))
    while l:
        arr.append(l.pop(0))
    while r:
        arr.append(r.pop(0))
    return arr

def mergeSort(arr):
    length=len(arr)
    mid_index=length//2
    if length<=1:
        return arr
    l=mergeSort(arr[mid_index:])
    r=mergeSort(arr[:mid_index])
    return merge(l,r)
L6=[0,9,8,7,6,5,4,3,2,1]
print('mergeSort:%s'%mergeSort(L6)) 


#堆排序
def heapify(heap,heap_size,root):
    left=root*2+1
    right=left+1
    larger=root
    if left<heap_size and heap[larger]<heap[left]:
        larger=left
    if right<heap_size and heap[larger]<heap[right]:
        larger=right
    if larger!=root:
        heap[larger],heap[root]=heap[root],heap[larger]
        heapify(heap,heap_size,larger)

def buildHeap(heap):
    heap_size=len(heap)
    for i in range((heap_size-2)//2,-1,-1):
        heapify(heap,heap_size,i)

def heapSort(heap):
    buildHeap(heap)
    for i in range(len(heap)-1,-1,-1):
        heap[i],heap[0]=heap[0],heap[i]
        heapify(heap, i, 0)
    return heap

L8=[0,9,8,7,6,5,4,3,2,1]
print('heapSort:%s'%heapSort(L8))