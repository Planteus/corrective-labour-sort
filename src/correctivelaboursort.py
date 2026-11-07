def reintegration(a, b):
    i = 0
    imax = len(a)
    j = 0
    jmax = len(b)
    result = []
    totallen = imax + jmax
    for k in range(totallen):
        if i == imax:
            result.append(b[j])
            j += 1
        elif j == jmax:
            result.append(a[i])
            i += 1
        elif a[i]<b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    return result

def sort(arr):
    return rehab(arr)

def rehab(arr):
    if not arr:
        return []
    if len(arr) == 1:
        return arr
    citizens, dissidents = findDissidents(arr)
    rehabbedCitizens = rehab(dissidents)
    idealPopulation = reintegration(citizens, rehabbedCitizens)
    return idealPopulation


def findDissidents(arr):
    citizens = [arr[0]]
    dissidents = []
    for i in range(1, len(arr)):
        if arr[i] >= citizens[-1]:
            citizens.append(arr[i])
        else:
            dissidents.append(arr[i])
    return citizens, dissidents


if __name__ == '__main__':
    print(sort([0, 4, -1, 9, 6, 2, 1, 5, 3, 8, 7]))