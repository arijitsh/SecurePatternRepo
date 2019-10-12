# Controller type: PID
import os
import numpy as np
import errno
############################## inputs ############################
modelName = "powersystem"

################## attack length and position ###################
innerCircleDepth = 0.1
pattern= 1
start = 1
isSat = 1
####################################################################
if modelName == "tempControl":
    modelName= "tempControl"
    A= np.matrix('0.94648514795348381856143760160194 0.0018971440127071483982418298452899;0 0.000000000013887943864964020896356969649573')
    B= np.matrix('-0.046752721484125708828472056666214;-0.99999999998611222018496391683584')
    C= np.matrix('1 0')
    D= np.matrix('0')
    Gain= np.matrix('-0.3712408426327057364702000086254 -0.0007441187601164687840174516431091')
    outerCircle = [30,30]
elif modelName == "powersystem":
    A= np.matrix('0.66 0.53;-0.53 0.13')
    B= np.matrix('0.34;0.53')
    C= np.matrix('1 0;0 1')
    D= np.matrix('0;0')
    Gain= np.matrix('0.0556 0.3306')
    outerCircle = [0.1,0.05]
elif modelName == "plant":
    A= np.matrix('2.6221    0.3197    1.8335   -1.0664; -0.2381    0.1872   -0.1361    0.2017; 0.1612    0.7888    0.2859    0.6064;-0.1035    0.7641    0.0886    0.7360')
    B= np.matrix('0.4654   -1.5495; 1.3138    0.0851; 2.0549   -0.6730; 2.0227   -0.1597')
    C= np.matrix('1     0     1    -1;0     1     0     0')
    D= np.matrix('0 0;0 0')
    Gain= np.matrix('-0.2580    0.3159   -0.1087    0.3982; -1.6195   -0.1314   -1.1232    0.7073')
    outerCircle = [0.01,0.01,0.01,0.01]
elif modelName == "powergrid":
    A= np.matrix('-1 -3;3 -5')
    B= np.matrix('2 -1;1 0')
    C= np.matrix('0.8 2.4;1.6 0.8')
    D= np.matrix('0 0; 0 0')
    Gain= np.matrix('2.9846   -4.9827;6.9635   -6.9599')
    outerCircle = [0.1,0.2]

################## creating the path to save results #################
path="../results/z3/"+modelName+"/"
try:
    os.makedirs(path)
except OSError as err:
    if err.errno!= errno.EEXIST:
        raise
#####################################################################
u_count=B.shape[1]
x_count=A.shape[1]

#Compute pattern length
patternLen=len(str(pattern))

#Compute pattern array
patternArray = np.zeros((patternLen), dtype=int)
patternTemp = pattern
i = patternLen-1
while patternTemp>0:
    patternArray[i] = patternTemp%10
    patternTemp=patternTemp//10
    i = i-1

####### Compute inner circle ##########################################################
innerCircle = np.zeros((x_count), dtype=float)
for i in range(x_count):
    innerCircle[i] = outerCircle[i]*innerCircleDepth

f0 = open(path+modelName+".z3result", "w+")
f0.write("1")
f0.close()

print("Finding IDS on time for "+str(modelName)+" and pattern "+str(pattern) + " with inner circle depth = "+str(innerCircleDepth))
K = start
while isSat == 1:  
    # create drop pattern    
    dropPattern = np.ones(K, dtype=int)
    j=0
    if pattern!=1:
        for i in range(K):
            dropPattern[i] = patternArray[j]
            j = j + 1
            if j == patternLen:
                j = 0
    print("drop pattern:")
    print(dropPattern)
    print("\n")
    fileName = modelName + "_" + str(innerCircleDepth) + "_" +str(K)+"_"+str(pattern)+".py"
    f = open(path+fileName, "w+")
    f.write("from z3 import *\n")
    f.write("import math\n")
    f.write("import numpy as np\n\n")
    f.write("s = Solver()\n")
    # f.write("set_option(precision=40)\n")
    f.write("set_option(rational_to_decimal=True)\n")

    for i in range(K+1):
        decl="\n"
        for varcount in range(1,x_count+1):
            decl+="x"+str(varcount)+"_"+str(i)+" = Real('x"+str(varcount)+"_"+str(i)+"')\n"
            decl+="z"+str(varcount)+"_"+str(i)+" = Real('z"+str(varcount)+"_"+str(i)+"')\n"
            decl+="xabs"+str(varcount)+"_"+str(i)+" = Real('xabs"+str(varcount)+"_"+str(i)+"')\n"

        for varcount in range(1,u_count+1):
            decl+="u"+str(varcount)+"_"+str(i)+" = Real('u"+str(varcount)+"_"+str(i)+"')\n"

        f.write(decl)
        
    f.write("\n")
    for varcount in range(1,x_count+1):
        f.write("s.add(x"+str(varcount)+"_0 < "+str(outerCircle[varcount-1])+")\n")
        f.write("s.add(x"+str(varcount)+"_0 > "+str(innerCircle[varcount-1])+")\n")
        f.write("s.add(xabs"+str(varcount)+"_0 == If(x"+str(varcount)+"_0<0,(-1)*x"+str(varcount)+"_0,x"+str(varcount)+"_0))\n")
    f.write("\n")

    j = 0
    for i in range(K):
        f.write("# pattern = "+str(dropPattern[i])+"\n")
        if dropPattern[i]==0:
            expr_u=""
            for varcount1 in range(1,u_count+1):
                expr_u+="s.add(u"+str(varcount1)+"_"+str(i)+" == u"+str(varcount1)+"_"+str(i-1)+")\n"
            f.write(expr_u)

        else:
            expr_u=""
            for varcount1 in range(1,u_count+1):
                expr_u+="s.add(u"+str(varcount1)+"_"+str(i)+" == "
                if i==0:
                    for varcount2 in range(1,x_count+1):
                        expr_u+="0"
                else:
                    for varcount2 in range(1,x_count+1):
                        expr_u+=" - ("+str(Gain[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i-1)+")"
                expr_u+=")\n"
            f.write(expr_u)
       
            
        expr_x=""
        expr_xabs=""
        for varcount1 in range(1,x_count+1):
            expr_x+="s.add(x"+str(varcount1)+"_"+str(i+1)+" == "    
            for varcount2 in range(1,x_count+1):
                expr_x+=" ("+str(A[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i)+") +"
            for varcount3 in range(1,u_count+1):
                expr_x+=" ("+str(B[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+") +"
            
            expr_xabs+="s.add(xabs"+str(varcount1)+"_"+str(i+1)+" == If(x"+str(varcount1)+"_"+str(i+1)+"<0,(-1)*x"+str(varcount1)+"_"+str(i+1)+",x"+str(varcount1)+"_"+str(i+1)+"))\n"

            expr_x=expr_x[:len(expr_x)-1] 
            expr_x = expr_x + ")\n"          

        f.write(expr_x)
        f.write(expr_xabs)
        
    f.write("s.add(Or(")
    assertion=""
    for varcount in range(1,x_count+1):
        assertion+="(xabs"+str(varcount)+"_"+str(K)+">"+str(innerCircle[varcount-1])+"),"
    assertion = assertion[:len(assertion)-1]
    f.write(assertion)
    f.write("))\n")

    # f.write("\nprint(s.sexpr())")
    f.write("\nif s.check() != sat:\n")
    f.write("\tprint(s.check())\n")
    f.write("\tisSat = 0\n")
    f.write("else:\n")
    f.write("\tprint(s.check())\n")
    f.write("\tisSat = 1\n")    

    f.write("if isSat==0:\n")
    f.write("\tf0 = open(\""+path+modelName+".z3result\", \"w+\")\n")
    f.write("\tf0.write(\"0\")\n")
    f.write("\tf0.close()\n")

    f.close()
    os.system("python "+path+fileName+">"+path+fileName+".z3out")
    f0 = open(path+modelName+".z3result", "r")
    if f0.mode == 'r':
        content = f0.read()
        isSat = int(content)
    f0.close()
    if isSat==1:
        os.system("rm -rf "+path+fileName+" "+path+fileName+".z3out")
    else:
        print("go to "+path+fileName+".z3out \n")
    K = K + 1