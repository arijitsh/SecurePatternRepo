# A Python program to print all 
# permutations using library function 
import itertools
from itertools import permutations 
from itertools import combinations, chain 

def findsubsets(s, n): 
    return list(map(set, itertools.combinations(s, n))) 

def get_uniques(links):    
    my_selection = links
    for l in links:
        if len(l)>1:
            for i in range(1,len(l)):
                sub_list = l[i:] + l[:i]
                if sub_list in links:
                    my_selection.remove(sub_list)
    return my_selection

def removeRateWise(links, rate):
    my_selection = []
    for l in links:
        ones = l.count('1')
        # print(l)
        # print(str((ones/len(l))))
        if (ones/len(l))>=rate and ones!=len(l):
            # print("selected")
            my_selection.append(l)
    return my_selection

arr = [1,11, 10, 100, 1000, 10000]
patternList = []
count = 0
for j in range(len(arr)):
    arr1 = findsubsets(arr, j+1)

    for k in range(len(arr1)):
        perm = list(permutations(arr1[k]))         
        for i in list(perm):             
            patternList.append(list(i))

# print(patternList)
unique = get_uniques(patternList)
pattern = []
for i in range(len(unique)):
    s = ""
    for element in unique[i]:
        s = s + str(element)
    pattern.append(s)
patternWithRate = removeRateWise(pattern, 0.5)

# print(patternWithRate)

oldPatternList = ['10','1100','110100','110010']
newPatternList = []
for p in patternWithRate:
    if p not in oldPatternList:
        newPatternList.append(p)

print(newPatternList)
