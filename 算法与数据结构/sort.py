#! /usr/bin/env python3


def qsorted(arr):
    if len(arr) <= 1:
        return arr
    less = []
    less_append = less.append
    equal = []
    equal_append = equal.append
    greater = []
    greater_append = greater.append
    pivot = arr[0]
    for each in arr:
        if each < pivot:
            less_append(each)
        elif each > pivot:
            greater_append(each)
        else:
            equal_append(each)
    return qsorted(less) + equal + qsorted(greater)


def merge_array(arr0, arr1):
    result = []
    m, n = 0, 0

    while m < len(arr0) and n < len(arr1):
        if arr0[m] < arr1[n]:
            result.append(arr0[m])
            m += 1
        else:
            result.append(arr1[n])
            n += 1
    result = result + arr0[m:] + arr1[n:]
    return result


def merge_array0(arr0, arr1):
    result = []
    m, n = 0, 0

    while m < len(arr0) and n < len(arr1):
        if arr0[m] < arr1[n]:
            result.append(arr0[m])
            m += 1
        elif arr0[m] == arr1[n]:
            result.append(arr0[m])
            m += 1
            n += 1
        else:
            result.append(arr1[n])
            n += 1
    result = result + arr0[m:] + arr1[n:]
    return result


if __name__ == "__main__":
    arr = qsorted([3, 6, 3, 1, 9, 5, 3, 1, 5])
    print(arr)

    arr0 = [1, 2, 6, 8, 10, 12]
    arr1 = [3, 6, 8, 9, 11, 14]
    rs = merge_array0(arr0, arr1)
    print(rs)
