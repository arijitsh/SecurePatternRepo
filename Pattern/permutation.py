# A Python program to print all 
# permutations using library function 
import itertools
from itertools import permutations 
from itertools import combinations, chain 

def findsubsets(s, n): 
    return list(map(set, itertools.combinations(s, n))) 

arr = [111, 10, 100, 1000, 10000]
patternList = []
count = 0
for j in range(len(arr)):
    arr1 = findsubsets(arr, j+1)

    if j<2:
        for k in range(len(arr1)):
            patternList.append(list(arr1[k]))
    else:
        for k in range(len(arr1)):
            perm = list(permutations(arr1[k]))        

    # Print the obtained permutations 
            for i in list(perm):             
                patternList.append(list(i))

print("count:"+str(count))
print("pattern list len:"+str(len(patternList)))
for i in range(len(patternList)):
    print(patternList[i])