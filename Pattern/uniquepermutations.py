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
        if float(ones)/len(l)>=rate and ones!=len(l):
            my_selection.append(l)
    return my_selection

####################################################################################################

basicArr = [1,10, 100, 1000, 10000]
# arr = [1,11, 111, 10, 1010, 100, 1000, 10000]
arr = [1,11, 111, 10, 1010, 100, 1000]

patternList = []
count = 0
for j in range(len(arr)):
    arr1 = findsubsets(arr, j+1)

    for k in range(len(arr1)):
        perm = list(permutations(arr1[k]))         
        for i in list(perm):             
            patternList.append(list(i))


unique = get_uniques(patternList)
pattern = []
for i in range(len(unique)):
    s = ""
    for element in unique[i]:
        s = s + str(element)
    pattern.append(s)

patternWithRate = removeRateWise(pattern, 0.5)

uniqueShiftPatterns = []
for i in range(len(patternWithRate)):
    k = 0
    a = patternWithRate[i]
    for j in range(len(a)):
        c = a[0:j]
        b = a[j:len(a)]+c[::-1]
        if b in uniqueShiftPatterns:
            k = k + 1
    if k== 0:
        uniqueShiftPatterns.append(a)


uniquePatterns = []

for q in uniqueShiftPatterns:
    k = 0
    for p in basicArr:
        c = q.count(str(p))
        if (c*len(str(p)) == len(q)):
            k=1
    if k==0:
        uniquePatterns.append(q)


finalPattern = []
for p in basicArr:
    q = str(p)
    ones = q.count('1')
    if float(ones)/len(q)>=0.5:
        finalPattern.append(q)
for p in uniquePatterns:
    finalPattern.append(p)





# this code removes already executed patterns
oldPatternList = ['1','10','1100','110100','110010','110', '1011', '11100', '100011', '11011', '11110', '111100', '110011', '1000111', '1000111', '10000111', '10000111', '1011100', '1010011', '10001011', '10001110', '11011100', '11010011', '11110100', '11110010', '11001011', '11001110', '100011011', '100011110', '100010111', '100010111', '100011110', '100011101', '1000011011', '1000011110', '1000010111', '1000010111', '1000011110', '1000011101', '1000111100', '1000110011', '1000111100', '1000111001', '1000100111', '1000100111', '110010001011', '110010001110', '110010100011', '110010111000', '110011100010', '110011101000', '110001001011', '110001001110', '110001010011', '110001011100', '110001110010', '110001110100', '110100100011', '110100111000', '110100010011', '110100011100', '110111001000', '110111000100', '111100100010', '111100101000', '111100010010', '111100010100', '111101001000', '111101000100']
newPatternList = []
for p in finalPattern:
    if p not in oldPatternList:
        newPatternList.append(p)

print(len(newPatternList))