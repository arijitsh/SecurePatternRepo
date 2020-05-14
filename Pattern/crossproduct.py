# Python program for cartesian 
# product of N-sets 

# function to find cartesian product of two sets 
def cartesianProduct(set_a, set_b): 
	result =[] 
	for i in range(0, len(set_a)): 
		for j in range(0, len(set_b)): 

			# for handling case having cartesian 
			# prodct first time of two sets 
			if type(set_a[i]) != list:		 
				set_a[i] = [set_a[i]] 
				
			# coping all the members 
			# of set_a to temp 
			temp = [num for num in set_a[i]] 
			
			# add member of set_b to 
			# temp to have cartesian product	 
			temp.append(set_b[j])			 
			result.append(temp) 
			
	return result 

# Function to do a cartesian 
# product of N sets 
def Cartesian(list_a, n): 
	
	# result of cartesian product 
	# of all the sets taken two at a time 
	temp = list_a[0] 
	
	# do product of N sets 
	for i in range(1, n): 
		temp = cartesianProduct(temp, list_a[i]) 
		
	print(temp) 

# Driver Code 
list_a = [[111, 10, 100, 1000],		 # set-1 
		[111, 10, 100, 1000],		 # set-2 
		[111, 10, 100, 1000],
        [111, 10, 100, 1000]] # set-3 
			
# number of sets 
n = len(list_a) 

# Function is called to perform 
# the cartesian product on list_a of size n 
Cartesian(list_a, n) 
