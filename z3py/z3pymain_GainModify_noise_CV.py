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

################### Reading number of sampling points ####################################################

with open('Time.csv','rt') as f:
  data = csv.reader(f)
  for row in data:
        r = str(row).replace('[','')
        r = r.replace(']','')
        r = r.replace('\'','')
        K = int(float(r))
print("Total number of iterations:"+str(K))

################ Reading the discrete state and constant matrices from the CSV file ##################################
A = np.zeros(shape=(10,10),dtype=float)
B = np.zeros(shape=(10,3),dtype=float)
H = np.zeros(shape=(5,10),dtype=float)
L = np.zeros(shape=(10,5),dtype=float)
X = np.zeros(shape=(K,10),dtype=float)
U = np.zeros(shape=(K),dtype=float)

i = 0
with open('A.csv','rt') as f:
  data = csv.reader(f)
  k = 0
  for row in data:
        r = str(row).replace('[','')
        r = r.replace(']','')
        r = r.replace('\'','')
        count = len(r.split(' '))
        for j in range(count):
            A[k][j] = float(r.split(' ')[j])
        k = k+1

i = 0
with open('B.csv','rt') as f:
  data = csv.reader(f)
  k = 0
  for row in data:
        r = str(row).replace('[','')
        r = r.replace(']','')
        r = r.replace('\'','')
        count = len(r.split(' '))
        for j in range(count):
            B[k][j] = float(r.split(' ')[j])
        k = k+1

i = 0
with open('X.csv','rt') as f:
  data = csv.reader(f)
  for row in data:
        r = str(row).replace('[','')
        r = r.replace(']','')
        r = r.replace('\'','')
        count = len(r.split(' '))
        for j in range(count):
            X[i][j] = float(r.split(' ')[j])
        i = i + 1

i = 0
with open('input.csv','rt') as f:
  data = csv.reader(f)
  for row in data:
        r = str(row).replace('[','')
        r = r.replace(']','')
        r = r.replace('\'','')
        count = len(r.split(' '))
        for j in range(count):
            U[j] = float(r.split(',')[j])

################## creating the path to save results #################
today = date.today()
dt = today.strftime("%b-%d-%Y")
path="results/"+dt+"/"
try:
    os.makedirs(path)
except OSError as err:
    if err.errno!= errno.EEXIST:
        raise

################# retreiving dimention of X, Y and U #################

u_count=3
x_count=10
z_count=5

################ Defining allowed limits of sensor data ##############
delta = 4
tau = 0.5

################ Defining safety bound ###############################
safety = 0.1
attackRange = 3.5

################## finding the attack points #########################
attackPoints = []
attackPoints.append((150,160))

########## Finding minimum attack length #############################
offset = 5
isSat = 1

print("Total number of steering change event:"+str(len(attackPoints)))
isAnyAttack = 1
attackVectorIndex = 0

while attackVectorIndex < attackVectorCount and isAnyAttack==1:
    isAnyAttack = 0

    print("Finding attack vector "+str(attackVectorIndex+1))

    for count in range(len(attackPoints)):
        print("Finding attack vector for duration number "+str(count+1))
        f0 = open(path+dt+"_downtime.z3result", "w+")
        f0.write("0")
        f0.close()    
        
        start = attackPoints[count][0] # start of the attack phase
        end = attackPoints[count][1] # end of the attack phase
        attackDuration = end-start
        counter = attackDuration # entire duration of interest

        isSat = 0
        attackLen = int(attackDuration)

        print("Activation duration starts at "+str(start)+" and ends at "+str(end))
        
        while attackLen<=counter and isSat == 0:
            print("Trying with attack length:"+str(attackLen))
            index = start  # index indicates the starting point of an attack        

            while (index + attackLen)<=end and (isSat == 0):
                print("Attack start at "+str(index))
                fileName1 = dt + "_GainModify_noise_" +str(start)+ "_"+str(attackLen)+"_WithRange"+str(attackRange)

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
                f.write("set_option(precision=40)\n")
                f.write("set_option(rational_to_decimal=True)\n")

                for varcount in range(1,x_count+1):
                    f.write("x"+str(varcount)+" = np.zeros("+str(counter+1)+", dtype=float)\n")
                for varcount in range(1,u_count+1):
                    f.write("u"+str(varcount)+" = np.zeros("+str(counter+1)+", dtype=float)\n")
                    
                f.write("attackOnKp = np.zeros("+str(counter+1)+", dtype=float)\n")  
                f.write("e1 = np.zeros("+str(counter+1)+", dtype=float)\n")
                f.write("e2 = np.zeros("+str(counter+1)+", dtype=float)\n")                

                for i in range(counter+1):
                    decl=""
                    for varcount in range(1,x_count+1):
                        decl+="x"+str(varcount)+"_"+str(i)+" = Real('x"+str(varcount)+"_"+str(i)+"')\n"

                    for varcount in range(1,u_count+1):
                        decl+="u"+str(varcount)+"_"+str(i)+" = Real('u"+str(varcount)+"_"+str(i)+"')\n"                    
                    
                    decl+= "e1_"+str(i)+" = Real('e1_"+str(i)+"')\n"
                    decl+= "e2_"+str(i)+" = Real('e2_"+str(i)+"')\n"

                    f.write(decl)
                    
                f.write("\n")
                for varcount in range(1,x_count+1):
                    f.write("s.add(x"+str(varcount)+"_0 == "+str(X[start][varcount-1])+")\n")
                for varcount2 in range(1,u_count+1):
                    if varcount2!=3:
                        f.write("s.add(u"+str(varcount2)+"_0 == 0)\n")
                    else:    
                        f.write("s.add(u3_0 == "+str(U[start])+")\n")
                f.write("\n")

                j = 0
                for i in range(counter):
                     # Applying attack on Kp gain component
                    expr_x=""
                    if i == (j+index - start):      # If in this iteration we can give an attack      
                        f.write("attackOnKp_"+str(i)+" = Real('attackOnKp_"+str(i)+"')\n")
                        f.write("s.add(And(attackOnKp_"+str(i)+"<"+str(attackRange)+",attackOnKp_"+str(i)+">-"+str(attackRange)+"))\n")
                        for varcount1 in range(1,x_count+1):
                            expr_x+="s.add(x"+str(varcount1)+"_"+str(i+1)+" == "
                            for varcount2 in range(1,x_count+1):
                                if varcount1 == 6 and varcount2 == 2:
                                    expr_x+=" (("+str(A[varcount1-1,varcount2-1])+"+attackOnKp_"+str(i)+")*x"+str(varcount2)+"_"+str(i)+") +"
                                elif varcount1 == 6 and varcount2 == 5:
                                    expr_x+=" (("+str(A[varcount1-1,varcount2-1])+"-attackOnKp_"+str(i)+")*x"+str(varcount2)+"_"+str(i)+") +"
                                elif varcount1 == 6 and varcount2 == 6:
                                    expr_x+=" (("+str(A[varcount1-1,varcount2-1])+"-(attackOnKp_"+str(i)+"*"+str(tau)+"))*x"+str(varcount2)+"_"+str(i)+") +"
                                else:
                                    expr_x+=" ("+str(A[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i)+") +"
                            for varcount3 in range(1,u_count+1):
                                expr_x+=" ("+str(B[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+") +"
                            
                            expr_x=expr_x[:len(expr_x)-1] 
                            expr_x = expr_x + ")\n" 

                        j = j+1
                        if j== attackLen:
                            j=0 
                    else:                        
                        for varcount1 in range(1,x_count+1):
                            expr_x+="s.add(x"+str(varcount1)+"_"+str(i+1)+" == "    
                            for varcount2 in range(1,x_count+1):
                                expr_x+=" ("+str(A[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i)+") +"
                            for varcount3 in range(1,u_count+1):
                                expr_x+=" ("+str(B[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+") +"
                            
                            expr_x=expr_x[:len(expr_x)-1] 
                            expr_x = expr_x + ")\n"       

                    f.write(expr_x)         

                    # update u
                    expr_u=""
                    for varcount1 in range(1,u_count+1):
                        if varcount1!=3:
                            expr_u+="s.add(u"+str(varcount1)+"_"+str(i+1)+" == 0)\n"
                        else:
                            expr_u+="s.add(u"+str(varcount1)+"_"+str(i+1)+" == "+str(U[i+1+start])+")\n"
                    f.write(expr_u)                        
                    
                    # Compute the error terms
                    expr_error = "s.add(e1_"+str(i+1)+" == (x4_"+str(i+1)+"-x7_"+str(i+1)+"-"+str(delta)+"-(x8_"+str(i+1)+"*"+str(tau)+"))/("+str(delta)+"+(x8_"+str(i+1)+"*"+str(tau)+")))\n"                        
                    expr_error += "s.add(e2_"+str(i+1)+" == (x1_"+str(i+1)+"-x4_"+str(i+1)+"-"+str(delta)+"-(x5_"+str(i+1)+"*"+str(tau)+"))/("+str(delta)+"+(x5_"+str(i+1)+"*"+str(tau)+")))\n"
                    
                    f.write(expr_error)

                # adding safety criteria
                expr_safety = "s.add(And("
                for i in range(counter):
                    expr_safety+="e1_"+str(i+1)+"<"+str(safety)+",e1_"+str(i+1)+">-"+str(safety)+",e2_"+str(i+1)+"<"+str(safety)+",e2_"+str(i+1)+">-"+str(safety)+","
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
                        expr_attak+= "attackOnKp_"+str(j-start)+"!="+str(line.split(',')[j])+","
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

                f.write("\t\tif \"attackOnKp_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\tattackOnKp[i] = float(y)\n")

                for varcount in range(1,u_count+1): # Parsing u, attack on u and attacked u values from the z3 py output
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
                f.write("\t\tprint(\"attackOnKp_{0}={1}\".format(i-1,attackOnKp[i-1]))\n")  
                for varcount in  range(1, x_count+1):
                    f.write("\t\tprint(\"x"+str(varcount)+"_{0}={1}\".format(i,x"+str(varcount)+"[i]))\n")                        
                for varcount in  range(1, u_count+1):
                    f.write("\t\tprint(\"u"+str(varcount)+"_{0}={1}\".format(i,u"+str(varcount)+"[i]))\n")                  
                f.write("\t\tprint(\"e1_{0}={1}\".format(i,e1[i]))\n")
                f.write("\t\tprint(\"e2_{0}={1}\".format(i,e2[i]))\n")
                    
                # Printing attack vectors
                f.write("print(\"attack on controller gain Kp\")\n")
                f.write("print(attackOnKp)\n")
                        
                # writing in CSV file                
                f.write("f1 = open(\""+path+fileName1+".csv\", \"a+\")\n")
                f.write("for i in range({0},{1}):\n".format(start,start+counter))
                f.write("\tf1.write(\"{0},\".format(attackOnKp[i-"+str(start)+"]))\n")
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