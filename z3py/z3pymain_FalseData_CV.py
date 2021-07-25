import csv, json
import numpy as np
import errno
import os
import platform
from datetime import date
import time
import sys

####################### Ask attack vector count and timeout from user ####################################################################
v = int(sys.version[0])

attackVectorCount = input("Max number of attack vector you want to generate:")

if v==3:
    while attackVectorCount.isnumeric()!=1 or int(attackVectorCount)<=0:
        print("Please enter a positive numeric value")
        attackVectorCount = input("Max number of attack vector you want to generate:")
    jsonFileMode = 'r'
else:
    while attackVectorCount<=0:
      print("Please enter a positive numeric value")
      attackVectorCount = input("Max number of attack vector you want to generate:")
    jsonFileMode = 'rU'

attackVectorCount = int(attackVectorCount)

######################## Detecting platform and setting command accordingly #############################
platformName = platform.system()

if platformName.upper() == "LINUX":
    removeCommand = "rm -rf "
if platformName.upper() == "WINDOWS":
    removeCommand = "del "

################################# Constant parameters and required input ################################

victim = 3 # 0 denotes platoon leader, 1 denotes 2nd vehicle, 2 denotes 3rd vehicle, and so on
noOfVehicles = 5

t = 0.1
delta = 4 
tau = 0.5 
c= [0.05 , 0.3 , 0.98 , -0.05 , -0.325 , -0.15]
r = 1

attackStart = 200
attackLen = 50

if noOfVehicles == 3:
    X = np.matrix('20;0;0;15;0;0;10;0;0;-0.2') # initial state
if noOfVehicles == 4:
    X = np.matrix('25;0;0;20;0;0;15;0;0;10;0;0;-0.2') # initial state
if noOfVehicles == 5:
    X = np.matrix('30;0;0;25;0;0;20;0;0;15;0;0;10;0;0;-0.2') # initial state


accProfile = 'input_sinusoid.csv'

# Defining safety bound 
safety = 0.2
attackRange = 2.5
accRange = 10

################### Reading number of sampling points ####################################################

with open(accProfile,'rt') as f:
  data = csv.reader(f)
  for row in data:
        K = len(str(row).split(','))
print("Total number of iterations:"+str(K))


################ Generating system matrices ##################################
A = np.zeros(shape=(noOfVehicles*3+1,noOfVehicles*3+1),dtype=float)
# if victim == 0:
#     B = np.zeros(shape=(noOfVehicles*3+1,1),dtype=float)
# else:
B = np.zeros(shape=(noOfVehicles*3+1,3),dtype=float)
U = np.zeros(shape=(K),dtype=float)

i = 0
j = 0
k = 0

while i< noOfVehicles*3:
    A[i][j] = 1
    A[i][j+1] = t
    A[i][j+2] = t*t/2
    A[i+1][j+1] = 1
    A[i+1][j+2] = t
    l = j-3
    if i+2 != 2:
        for k in range(6):
            A[i+2][l] = c[k]
            l = l + 1
        A[i+2][noOfVehicles*3] = r
    i = i + 3
    j = j + 3

A[noOfVehicles*3][noOfVehicles*3] = r
# print(A)
# if victim == 0:
#     B[2] = 1
# else:
B[2][2] = 1
B[(victim+2)*3-1][0] = A[(victim+2)*3-1][(victim+1)*3-1]
print(B)
##################### Reading acceleration of platoon leader from acceleration profile file ##########################

with open(accProfile,'rt') as f:
  data = csv.reader(f)
  for row in data:
        l = str(row).replace('[','')
        l = l.replace(']','')
        l = l.replace('\'','')
        count = len(l.split(' '))
        for j in range(count):
            U[j] = float(l.split(',')[j])

################## creating the path to save results ######################################################
today = date.today()
dt = today.strftime("%b-%d-%Y")
path="results/"+dt+"/"
try:
    os.makedirs(path)
except OSError as err:
    if err.errno!= errno.EEXIST:
        raise

################# retreiving dimention of X, Y and U #################

# if victim == 0:
#     u_count = 1
#     u_actual = 0
# else:
u_actual = np.zeros(shape=(3,1),dtype=float)
u_count = 3

x_count=noOfVehicles*3+1

################## finding the attack points #########################
attackPoints = []
attackPoints.append((attackStart,attackStart+attackLen))

########################## state progression upto attack onset ###########3
for i in range(attackStart):
    # if victim != 0:
    u_actual[2][0] = U[i]
    # else:
    #     u_actual = U[i]
    X = np.dot(A,X) + np.dot(B,u_actual)
########## Finding attack vector #############################
isSat = 1

print("Total number of target attack area:"+str(len(attackPoints)))
isAnyAttack = 1
attackVectorIndex = 0

while attackVectorIndex < attackVectorCount and isAnyAttack==1:
    isAnyAttack = 0

    print("Finding attack vector "+str(attackVectorIndex+1))

    for count in range(len(attackPoints)):
        print("Finding attack vector for target area number "+str(count+1))
        f0 = open(path+dt+"_downtime.z3result", "w+")
        f0.write("0")
        f0.close()    
        
        start = attackPoints[count][0] # start of the attack phase
        end = attackPoints[count][1] # end of the attack phase
        attackDuration = end-start
        counter = attackDuration # entire duration of interest

        isSat = 0
        attackLen = attackDuration

        print("Activation duration starts at "+str(attackStart)+" and ends at "+str(end))
        
        while attackLen<=counter and isSat == 0:
            print("Trying with attack length:"+str(attackLen))
            index = start  # index indicates the starting point of an attack        

            while (index + attackLen)<=end and (isSat == 0):
                print("Attack start at "+str(index))
                if accProfile == "input_sinusoid.csv":
                    acc = "sinusoid"
                else:
                    acc = "abrupt"
                fileName1 = dt + "_FalseData_" +str(acc)+"_" +str(victim+1)+"outOf"+str(noOfVehicles)+"_"+str(start)+ "_"+str(attackLen)+"_"+str(attackRange)+"_"+str(safety)

                f1 = open(path+fileName1+".csv", "a+")
                for i in range(start):
                    f1.write("0,")
                f1.close()              

                fileName =fileName1+".py"
                f = open(path+fileName, "w+")               
                f.write("from z3 import *\n")
                f.write("import math\n")
                f.write("import numpy as np\n\n")
                f.write("s = Solver()\n")
                f.write("set_option(precision=10)\n")
                f.write("set_option(rational_to_decimal=True)\n")

                for varcount in range(1,x_count+1):
                    f.write("x"+str(varcount)+" = np.zeros("+str(counter+1)+", dtype=float)\n")
                for varcount in range(1,u_count+1):
                    f.write("u"+str(varcount)+" = np.zeros("+str(counter+1)+", dtype=float)\n")
                    f.write("uattacked"+str(varcount)+" = np.zeros("+str(counter+1)+", dtype=float)\n")
                    
                f.write("attackOnU = np.zeros("+str(counter+1)+", dtype=float)\n")  
                
                for varcount in range(1,noOfVehicles):
                    f.write("e"+str(varcount)+" = np.zeros("+str(counter+1)+", dtype=float)\n")            

                for i in range(counter+1):
                    decl=""
                    for varcount in range(1,x_count+1):
                        decl+="x"+str(varcount)+"_"+str(i)+" = Real('x"+str(varcount)+"_"+str(i)+"')\n"

                    for varcount in range(1,u_count+1):
                        decl+="u"+str(varcount)+"_"+str(i)+" = Real('u"+str(varcount)+"_"+str(i)+"')\n"
                        decl+="uattacked"+str(varcount)+"_"+str(i)+" = Real('uattacked"+str(varcount)+"_"+str(i)+"')\n"
                    
                    for varcount in range(1,noOfVehicles):
                        decl+= "e"+str(varcount)+"_"+str(i)+" = Real('e"+str(varcount)+"_"+str(i)+"')\n"

                    f.write(decl)
                    
                f.write("\n")
                for varcount in range(1,x_count+1):
                    f.write("s.add(x"+str(varcount)+"_0 == "+str(round(X.item(varcount-1),10))+")\n")
                    # f.write("s.add(x"+str(varcount)+"_0 == "+str(X[varcount-1])+")\n")

                # if victim == 0:
                #     f.write("s.add(u1_0 == "+str(U[start])+")\n")
                #     f.write("s.add(uattacked1_0 == u1_0)\n")
                # else:
                for varcount2 in range(1,u_count+1):
                    if varcount2!=3:
                        f.write("s.add(u"+str(varcount2)+"_0 == 0)\n")
                    else:    
                        f.write("s.add(u"+str(varcount2)+"_0 == "+str(U[start])+")\n")
                    f.write("s.add(uattacked"+str(varcount2)+"_0 == u"+str(varcount2)+"_0)\n")
                f.write("\n")

                j = 0
                for i in range(counter):

                    # Update x
                    expr_x=""
                    for varcount1 in range(1,x_count+1):
                        expr_x+="s.add(x"+str(varcount1)+"_"+str(i+1)+" == "                
                        for varcount2 in range(1,x_count+1):
                            expr_x+=" ("+str(round(A[varcount1-1,varcount2-1],10))+"*x"+str(varcount2)+"_"+str(i)+") +"
                        for varcount3 in range(1,u_count+1):
                            expr_x+=" ("+str(round(B[varcount1-1,varcount3-1],10))+"*uattacked"+str(varcount3)+"_"+str(i)+") +"
                                                    
                        expr_x=expr_x[:len(expr_x)-1] 
                        expr_x = expr_x + ")\n"
                        
                    f.write(expr_x)          

                    # update u
                    expr_u=""
                    # if victim == 0:
                    #     expr_u+="s.add(u1_"+str(i+1)+" == "+str(U[i+1+start])+")\n"
                    # else:
                    for varcount1 in range(1,u_count+1):
                        if varcount1!=3:
                            expr_u+="s.add(u"+str(varcount1)+"_"+str(i+1)+" == 0)\n"
                        else:
                            expr_u+="s.add(u"+str(varcount1)+"_"+str(i+1)+" == "+str(U[i+1+start])+")\n"
                    f.write(expr_u)

                    # Applying attack on u
                    if i == (j+index - start):      # If in this iteration we can give an attack      
                        expr_uatk=""
                        f.write("attackOnU_"+str(i)+" = Real('attackOnU_"+str(i)+"')\n")
                        # if victim == 0:
                        #     expr_uatk+="s.add(uattacked1_"+str(i+1)+" == u1_"+str(i+1)+" + attackOnU_"+str(i)+")\n"
                        #     # expr_uatk+="s.add(And(uattacked1_"+str(i+1)+"<="+str(accRange)+",uattacked1_"+str(i+1)+">=-"+str(accRange)+"))\n"
                        # else:
                        for varcount1 in range(1,u_count+1):
                            if varcount1!=1:
                                expr_uatk+="s.add(uattacked"+str(varcount1)+"_"+str(i+1)+" == u"+str(varcount1)+"_"+str(i+1)+")\n"
                            else:
                                expr_uatk+="s.add(uattacked"+str(varcount1)+"_"+str(i+1)+" == u"+str(varcount1)+"_"+str(i+1)+" + attackOnU_"+str(i)+")\n"
                                # expr_uatk+="s.add(And(uattacked"+str(varcount1)+"_"+str(i+1)+"<="+str(accRange)+",uattacked"+str(varcount1)+"_"+str(i+1)+">=-"+str(accRange)+"))\n"
                        
                        f.write(expr_uatk)
                        f.write("s.add(And(attackOnU_"+str(i)+"<="+str(attackRange)+",attackOnU_"+str(i)+">=-"+str(attackRange)+"))\n")
                        
                        j = j+1
                        if j== attackLen:
                            j=0 
                    else:
                        expr_u=""
                        for varcount1 in range(1,u_count+1):
                            expr_u+="s.add(uattacked"+str(varcount1)+"_"+str(i+1)+" == u"+str(varcount1)+"_"+str(i+1)+")\n"
                        f.write(expr_u)
                                        
                    # Compute the error terms
                    expr_error = ""

                    for varcount in range(1, noOfVehicles):
                        varcount2 = (varcount - 1)*3 + 1
                        expr_error+="s.add(e"+str(varcount)+"_"+str(i+1)+" == (x"+str(varcount2)+"_"+str(i+1)+"-x"+str(varcount2+3)+"_"+str(i+1)+"-"+str(delta)+"-(x"+str(varcount2+4)+"_"+str(i+1)+"*"+str(tau)+"))/("+str(delta)+"+(x"+str(varcount2+4)+"_"+str(i+1)+"*"+str(tau)+")))\n"                        
                    
                    f.write(expr_error)

                # adding safety criteria
                expr_safety = "s.add(Or("
                for i in range(counter):
                    for j in range(1, noOfVehicles):
                        # expr_safety+="e"+str(j)+"_"+str(i+1)+">"+str(safety)+","
                        expr_safety+="e"+str(j)+"_"+str(i+1)+"<-"+str(safety)+",e"+str(j)+"_"+str(i+1)+">"+str(safety)+","
                expr_safety = expr_safety[:len(expr_safety)-1]
                expr_safety+="))\n"

                f.write(expr_safety)                   

                # Nullify previous attack vectors
                f1 = open(path+fileName1+".csv", "a+")
                expr_attak = ""

                for i in range(attackVectorIndex):
                    line = f1.readline()
                    expr_attak+="s.add(And("
                    for j in range(index, index+attackLen):
                        expr_attak+= "attackOnU_"+str(j-start)+"!="+str(line.split(',')[j])+","
                    expr_attak = expr_attak[0:len(expr_attak)-1]
                    expr_attak+="))\n"
                f1.close()

                f.write(expr_attak)


                # # f.write("\nprint(s.sexpr())")
                f.write("\nsatcheck = s.check()\n")
                f.write("if satcheck != sat:\n")
                f.write("\tprint(satcheck)\n")
                f.write("\tisSat = 0\n")
                f.write("else:\n")
                f.write("\tprint(satcheck)\n")
                f.write("\tisSat = 1\n")
                f.write("\tf0 = open(\""+path+dt+"_downtime.z3result\", \"w+\")\n")
                f.write("\tf0.write(\"1\")\n")
                f.write("\tf0.close()\n") 
                f.write("\tm = s.model()\n")
                f.write("\tfor d in m.decls():\n")
                # f.write("\t\tprint (\"%s = %s\" % (d.name(), m[d]))\n")
                f.write("\t\tif \"e1_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\te1[i] = float(y)\n")

                f.write("\t\tif \"e2_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\te2[i] = float(y)\n")

                f.write("\t\tif \"attackOnU_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\tattackOnU[i] = float(y)\n")

                for varcount in range(1,u_count+1): # Parsing u, attack on u and attacked u values from the z3 py output
                    f.write("\t\tif \"uattacked"+str(varcount)+"_\" in d.name():\n")
                    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                    f.write("\t\t\tx = str(m[d])\n")
                    f.write("\t\t\tindex = x.find(\"?\")\n")
                    f.write("\t\t\tif index != -1:\n")
                    f.write("\t\t\t\ty = x[:-1]\n")
                    f.write("\t\t\telse:\n")
                    f.write("\t\t\t\ty = x\n")
                    f.write("\t\t\tuattacked"+str(varcount)+"[i] = float(y)\n")

                    f.write("\t\tif \"u"+str(varcount)+"_\" in d.name():\n")
                    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                    f.write("\t\t\tx = str(m[d])\n")
                    f.write("\t\t\tindex = x.find(\"?\")\n")
                    f.write("\t\t\tif index != -1:\n")
                    f.write("\t\t\t\ty = x[:-1]\n")
                    f.write("\t\t\telse:\n")
                    f.write("\t\t\t\ty = x\n")
                    f.write("\t\t\tu"+str(varcount)+"[i] = float(y)\n")
                for varcount in range(1,x_count+1): # Parsing x, absolute x and z from z3 py output
                    f.write("\t\tif \"x"+str(varcount)+"_\" in d.name():\n")
                    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                    f.write("\t\t\tx = str(m[d])\n")
                    f.write("\t\t\tindex = x.find(\"?\")\n")
                    f.write("\t\t\tif index != -1:\n")
                    f.write("\t\t\t\ty = x[:-1]\n")
                    f.write("\t\t\telse:\n")
                    f.write("\t\t\t\ty = x\n")
                    f.write("\t\t\tx"+str(varcount)+"[i] = float(y)\n")                      

                # Printing the execution sequence
                f.write("\tfor i in range(1,{0}):\n".format(counter+1))
                for varcount in  range(1, x_count+1):
                    f.write("\t\tprint(\"x"+str(varcount)+"_{0}={1}\".format(i,x"+str(varcount)+"[i]))\n")                    
                for varcount in  range(1, u_count+1):
                    f.write("\t\tprint(\"u"+str(varcount)+"_{0}={1}\".format(i,u"+str(varcount)+"[i]))\n")  
                f.write("\t\tprint(\"attackOnU_{0}={1}\".format(i-1,attackOnU[i-1]))\n")  
                for varcount in  range(1, u_count+1):
                    f.write("\t\tprint(\"uattacked"+str(varcount)+"_{0}={1}\".format(i,uattacked"+str(varcount)+"[i]))\n")
                f.write("\t\tprint(\"e1_{0}={1}\".format(i,e1[i]))\n")
                f.write("\t\tprint(\"e2_{0}={1}\".format(i,e2[i]))\n")
                    
                # Printing attack vectors
                f.write("print(\"attack on control signal component {0}\")\n".format(3))
                f.write("print(attackOnU)\n")
                        
                # writing in CSV file                
                f.write("f1 = open(\""+path+fileName1+".csv\", \"a+\")\n")
                f.write("for i in range({0},{1}):\n".format(start,start+counter))
                f.write("\tf1.write(\"{0},\".format(attackOnU[i-"+str(start)+"]))\n")
                f.write("f1.close()\n")

                f.write("if isSat==1:\n")
                f.write("\tf0 = open(\""+path+dt+"_downtime.z3result\", \"w+\")\n")
                f.write("\tf0.write(\"1\")\n")
                f.write("\tf0.close()\n")

                f.close()
                os.system("python "+path+fileName+">"+path+fileName1+".z3out")                

                f0 = open(path+dt+"_downtime.z3result", "r")
                if f0.mode == 'r':
                    content = f0.read()
                    isSat = int(content)
                f0.close()
                print("isSat="+str(isSat))
                if isSat==0:
                    print("attack vector not found")
                    os.system(removeCommand+path+fileName1+".csv")                    
                else:
                    attackVectorIndex = attackVectorIndex + 1
                    isAnyAttack = 1
                    print("attack vectors can be found in "+path)

                    #post processing
                    f1 = open(path+fileName1+".csv", "a+")
                    for i in range(start+attackLen,K):
                        f1.write("0")
                        if i!=K-1:
                            f1.write(",")
                        else:
                            f1.write("\n")
                    f1.close()

                    print("go to "+path+fileName1+".z3out \n")                             
                
                # os.system(removeCommand+path+fileName+" "+path+fileName1+".z3out")
                index = index + 1
            attackLen = attackLen + 1