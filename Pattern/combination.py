# Function which returns subset or r length from n 
from itertools import combinations 

def rSubset(arr, r): 

	# return list of all subsets of length r 
	# to deal with duplicate subsets use 
	# set(list(combinations(arr, r))) 
	return list(combinations(arr, r)) 

# Driver Function 
if __name__ == "__main__": 
	arr = [111, 10, 100, 1000] 
	r = 1
	print(rSubset(arr, r) )
